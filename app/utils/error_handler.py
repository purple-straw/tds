"""
错误处理模块
"""
from flask import jsonify
from app.utils.log_control import ERROR
from sqlalchemy.exc import SQLAlchemyError
from pymysql.err import MySQLError
import traceback


def handle_error(error, status_code=500):
    """
    统一处理错误并返回标准格式的错误响应
    
    Args:
        error: 错误信息或异常对象
        status_code: HTTP状态码，默认500
        
    Returns:
        tuple: (JSON响应, 状态码)
    """
    error_message = str(error)
    error_type = type(error).__name__
    
    # 获取堆栈跟踪信息
    stack_trace = traceback.format_exc()
    
    # 记录错误日志
    ERROR.logger.error(f"错误类型: {error_type}")
    ERROR.logger.error(f"错误信息: {error_message}")
    ERROR.logger.error(f"堆栈跟踪:\n{stack_trace}")
    
    # 根据错误类型设置适当的状态码和消息
    if isinstance(error, (SQLAlchemyError, MySQLError)):
        status_code = 503
        error_message = "数据库操作失败"
    elif isinstance(error, ValueError):
        status_code = 400
        # 保持原始错误消息
    elif isinstance(error, KeyError):
        status_code = 400
        error_message = "缺少必要的参数"
    elif isinstance(error, FileNotFoundError):
        status_code = 404
        error_message = "请求的资源不存在"
    elif isinstance(error, PermissionError):
        status_code = 403
        error_message = "没有权限执行该操作"
    elif isinstance(error, TimeoutError):
        status_code = 504
        error_message = "操作超时"
    
    # 构建错误响应
    error_response = {
        "error": {
            "type": error_type,
            "message": error_message,
            "code": status_code
        }
    }
    
    # 在开发环境下添加堆栈跟踪
    if ERROR.logger.getEffectiveLevel() <= 10:  # DEBUG level
        error_response["error"]["stack_trace"] = stack_trace
    
    return jsonify(error_response), status_code


def handle_validation_error(errors):
    """
    处理数据验证错误
    
    Args:
        errors: 验证错误信息
        
    Returns:
        tuple: (JSON响应, 状态码)
    """
    ERROR.logger.error(f"数据验证错误: {errors}")
    
    error_response = {
        "error": {
            "type": "ValidationError",
            "message": "数据验证失败",
            "details": errors,
            "code": 400
        }
    }
    
    return jsonify(error_response), 400


def handle_api_error(response):
    """
    处理API调用错误
    
    Args:
        response: API响应对象
        
    Returns:
        tuple: (JSON响应, 状态码)
    """
    status_code = response.status_code
    
    try:
        error_data = response.json()
    except ValueError:
        error_data = {"message": response.text}
    
    ERROR.logger.error(f"API调用错误: {error_data}")
    
    error_response = {
        "error": {
            "type": "APIError",
            "message": "API调用失败",
            "details": error_data,
            "code": status_code
        }
    }
    
    return jsonify(error_response), status_code

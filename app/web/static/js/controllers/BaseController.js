export class BaseController {
    constructor() {
        this.elements = {};
    }

    // 获取DOM元素的通用方法
    getElement(selector) {
        if (!this.elements[selector]) {
            this.elements[selector] = document.querySelector(selector);
        }
        return this.elements[selector];
    }

    // 显示提示信息
    showToast(message, type = 'info') {
        // 创建toast元素
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.textContent = message;
        
        // 添加到页面
        document.body.appendChild(toast);
        
        // 动画显示
        setTimeout(() => toast.classList.add('show'), 10);
        
        // 3秒后移除
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // 显示错误信息
    showError(message) {
        this.showToast(message, 'error');
    }

    // 显示加载中状态
    showLoading(element) {
        element.innerHTML = `
            <div class="loading-spinner">
                <div class="spinner"></div>
                <span>加载中...</span>
            </div>
        `;
    }

    // 密码验证
    showPasswordPrompt(callback) {
        const modalHtml = `
            <div class="modal fade" id="passwordModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">请输入密码</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="form-group">
                                <input type="password" class="form-control" id="password-input" placeholder="请输入密码">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary" id="confirm-password">确认</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('passwordModal'));
        modal.show();

        const handlePassword = () => {
            const password = document.getElementById('password-input').value;
            if (password === '10086') {
                modal.hide();
                if (callback) callback();
            } else {
                this.showError('密码错误！');
            }
        };

        // 处理密码确认
        document.getElementById('confirm-password').addEventListener('click', handlePassword);

        // 添加回车键支持
        document.getElementById('password-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                handlePassword();
            }
        });

        // 模态框关闭时清理
        document.getElementById('passwordModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }
} 
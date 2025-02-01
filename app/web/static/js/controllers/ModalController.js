import { BaseController } from './BaseController.js';

export class ModalController extends BaseController {
    constructor() {
        super();
        this.activeModal = null;
        this.modalStack = [];
    }

    // 创建模态框
    createModal(options = {}) {
        const {
            id = 'modal-' + Date.now(),
            title = '',
            content = '',
            size = '', // '', 'modal-lg', 'modal-xl', 'modal-sm'
            buttons = [],
            closeButton = true,
            backdrop = true,
            keyboard = true,
            onShow = null,
            onHide = null,
            onConfirm = null
        } = options;

        const modalHtml = `
            <div class="modal fade" id="${id}" tabindex="-1" data-bs-backdrop="${backdrop}" data-bs-keyboard="${keyboard}">
                <div class="modal-dialog ${size}">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">${title}</h5>
                            ${closeButton ? '<button type="button" class="btn-close" data-bs-dismiss="modal"></button>' : ''}
                        </div>
                        <div class="modal-body">
                            ${content}
                        </div>
                        ${this.generateFooter(buttons)}
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modalElement = document.getElementById(id);
        const modal = new bootstrap.Modal(modalElement, {
            backdrop,
            keyboard
        });

        // 绑定事件
        if (onShow) {
            modalElement.addEventListener('shown.bs.modal', onShow);
        }
        
        if (onHide) {
            modalElement.addEventListener('hidden.bs.modal', onHide);
        }

        // 绑定按钮事件
        buttons.forEach(button => {
            if (button.id) {
                const buttonElement = modalElement.querySelector(`#${button.id}`);
                if (buttonElement && button.onClick) {
                    buttonElement.addEventListener('click', (e) => button.onClick(e, modal));
                }
            }
        });

        // 确认按钮事件
        if (onConfirm) {
            const confirmButton = modalElement.querySelector('.btn-confirm');
            if (confirmButton) {
                confirmButton.addEventListener('click', () => onConfirm(modal));
            }
        }

        // 自动清理
        modalElement.addEventListener('hidden.bs.modal', function () {
            this.remove();
        });

        return modal;
    }

    // 生成模态框底部按钮
    generateFooter(buttons) {
        if (!buttons || buttons.length === 0) return '';

        const buttonHtml = buttons.map(button => `
            <button type="button" 
                id="${button.id || ''}"
                class="btn ${button.class || 'btn-secondary'}"
                ${button.dismiss ? 'data-bs-dismiss="modal"' : ''}>
                ${button.icon ? `<i class="${button.icon}"></i> ` : ''}${button.text}
            </button>
        `).join('');

        return `
            <div class="modal-footer">
                ${buttonHtml}
            </div>
        `;
    }

    // 显示确认对话框
    showConfirm(options = {}) {
        const {
            title = '确认',
            message = '确定要执行此操作吗？',
            confirmText = '确定',
            cancelText = '取消',
            confirmClass = 'btn-primary',
            onConfirm = null,
            onCancel = null
        } = options;

        return this.createModal({
            title,
            content: `<p>${message}</p>`,
            buttons: [
                {
                    text: cancelText,
                    class: 'btn-secondary',
                    dismiss: true,
                    onClick: (e, modal) => {
                        if (onCancel) onCancel();
                    }
                },
                {
                    text: confirmText,
                    class: confirmClass,
                    onClick: (e, modal) => {
                        if (onConfirm) onConfirm();
                        modal.hide();
                    }
                }
            ]
        });
    }

    // 显示表单模态框
    showFormModal(options = {}) {
        const {
            title = '表单',
            fields = [],
            onSubmit = null,
            submitText = '提交',
            cancelText = '取消',
            size = 'modal-lg'
        } = options;

        const formContent = `
            <form id="modalForm">
                ${fields.map(field => this.generateFormField(field)).join('')}
            </form>
        `;

        return this.createModal({
            title,
            content: formContent,
            size,
            buttons: [
                {
                    text: cancelText,
                    class: 'btn-secondary',
                    dismiss: true
                },
                {
                    text: submitText,
                    class: 'btn-primary',
                    onClick: async (e, modal) => {
                        if (onSubmit) {
                            const form = document.getElementById('modalForm');
                            const formData = new FormData(form);
                            const data = Object.fromEntries(formData.entries());
                            
                            try {
                                await onSubmit(data);
                                modal.hide();
                            } catch (error) {
                                this.showError(error.message);
                            }
                        }
                    }
                }
            ]
        });
    }

    // 生成表单字段
    generateFormField(field) {
        const {
            type = 'text',
            name,
            label,
            value = '',
            required = false,
            options = [],
            placeholder = ''
        } = field;

        if (type === 'select') {
            return `
                <div class="mb-3">
                    <label class="form-label">${label}</label>
                    <select class="form-select" name="${name}" ${required ? 'required' : ''}>
                        ${options.map(option => `
                            <option value="${option.value}" ${value === option.value ? 'selected' : ''}>
                                ${option.text}
                            </option>
                        `).join('')}
                    </select>
                </div>
            `;
        }

        return `
            <div class="mb-3">
                <label class="form-label">${label}</label>
                <input type="${type}" 
                       class="form-control" 
                       name="${name}" 
                       value="${value}"
                       placeholder="${placeholder}"
                       ${required ? 'required' : ''}>
            </div>
        `;
    }

    // 显示加载中模态框
    showLoading(message = '加载中...') {
        return this.createModal({
            content: `
                <div class="text-center">
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-2">${message}</p>
                </div>
            `,
            closeButton: false,
            backdrop: 'static',
            keyboard: false
        });
    }

    // 显示消息模态框
    showMessage(options = {}) {
        const {
            title = '提示',
            message = '',
            type = 'info', // 'info', 'success', 'warning', 'danger'
            confirmText = '确定'
        } = options;

        return this.createModal({
            title,
            content: `
                <div class="alert alert-${type} mb-0">
                    ${message}
                </div>
            `,
            buttons: [
                {
                    text: confirmText,
                    class: `btn-${type}`,
                    dismiss: true
                }
            ]
        });
    }
} 
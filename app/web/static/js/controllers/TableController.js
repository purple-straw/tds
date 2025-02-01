import { BaseController } from './BaseController.js';
import { ApiService } from '../services/ApiService.js';

export class TableController extends BaseController {
    constructor() {
        super();
        this.apiService = new ApiService();
        this.elements = {
            tableHeaders: '#table-headers',
            tableBody: '#table-body',
            tableContainer: '#table-container',
            iframeContainer: '#iframe-container'
        };
        
        this.headers = ['ID', '姓名', '职级', '性别', '员工工号', '职位', '入职日期', '状态', '操作'];
    }

    // 初始化表格
    async initialize() {
        try {
            const data = await this.apiService.getDbData();
            this.displayTableData(data.data);
        } catch (error) {
            this.showError('加载数据失败：' + error.message);
        }
    }

    // 显示表格数据
    displayTableData(data) {
        const tableHeaders = this.getElement(this.elements.tableHeaders);
        const tableBody = this.getElement(this.elements.tableBody);
        
        // 清空现有内容
        tableHeaders.innerHTML = '';
        tableBody.innerHTML = '';
        
        // 添加表头
        const headerFields = ['id', 'name', 'level', 'gender', 'per_code', 'manage_name', 'join_work_date', 'status', 'actions'];
        const headerLabels = ['ID', '姓名', '职级', '性别', '员工工号', '职位', '入职日期', '状态', '操作'];
        
        headerFields.forEach((field, index) => {
            const th = document.createElement('th');
            th.textContent = headerLabels[index];
            th.setAttribute('data-field', field);
            tableHeaders.appendChild(th);
        });
        
        // 如果没有数据，显示提示信息
        if (!data || !Array.isArray(data) || data.length === 0) {
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = headerFields.length;
            td.textContent = '暂无数据';
            td.style.textAlign = 'center';
            tr.appendChild(td);
            tableBody.appendChild(tr);
            return;
        }
        
        // 添加数据行
        data.forEach(row => {
            const tr = document.createElement('tr');
            [
                { field: 'id', value: row.id },
                { field: 'name', value: row.name },
                { field: 'level', value: row.level },
                { field: 'gender', value: row.gender },
                { field: 'per_code', value: row.per_code },
                { field: 'manage_name', value: row.manage_name },
                { field: 'join_work_date', value: row.join_work_date },
                { field: 'status', value: row.status }
            ].forEach(({field, value}) => {
                const td = document.createElement('td');
                td.setAttribute('data-field', field);
                td.textContent = value || '-';
                tr.appendChild(td);
            });

            // 添加操作列
            const actionTd = document.createElement('td');
            actionTd.setAttribute('data-field', 'actions');
            actionTd.innerHTML = `
                <div class="btn-group">
                    <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${row.id}">
                        <i class="fas fa-edit"></i> 编辑
                    </button>
                    <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${row.id}">
                        <i class="fas fa-trash"></i> 删除
                    </button>
                </div>
            `;
            tr.appendChild(actionTd);
            
            tableBody.appendChild(tr);
        });

        // 添加事件监听
        document.querySelectorAll('.edit-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const rowId = e.currentTarget.dataset.id;
                this.showPasswordPrompt(() => this.showEditForm(rowId));
            });
        });

        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const rowId = e.currentTarget.dataset.id;
                this.showPasswordPrompt(() => this.handleDelete(rowId));
            });
        });
    }

    // 显示编辑表单
    showEditForm(rowData) {
        const modalHtml = `
            <div class="modal fade" id="editModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">编辑人员信息</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <form id="editForm">
                                ${this.generateFormFields(rowData)}
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary" id="save-edit">保存</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('editModal'));
        modal.show();

        // 处理表单提交
        this.handleFormSubmit(rowData.id, modal);
    }

    // 生成表单字段
    generateFormFields(data) {
        const fields = [
            { name: 'name', label: '姓名', type: 'text', required: true },
            { name: 'level', label: '职级', type: 'text', required: true },
            { name: 'gender', label: '性别', type: 'select', options: ['男', '女'], required: true },
            { name: 'per_code', label: '员工工号', type: 'text', required: true },
            { name: 'manage_name', label: '职位', type: 'text', required: true },
            { name: 'join_work_date', label: '入职日期', type: 'date', required: true },
            { name: 'status', label: '状态', type: 'text', required: true }
        ];

        return fields.map(field => {
            if (field.type === 'select') {
                return `
                    <div class="mb-3">
                        <label class="form-label">${field.label}</label>
                        <select class="form-select" name="${field.name}" ${field.required ? 'required' : ''}>
                            ${field.options.map(option => `
                                <option value="${option}" ${data && data[field.name] === option ? 'selected' : ''}>
                                    ${option}
                                </option>
                            `).join('')}
                        </select>
                    </div>
                `;
            }
            
            return `
                <div class="mb-3">
                    <label class="form-label">${field.label}</label>
                    <input type="${field.type}" class="form-control" name="${field.name}" 
                           value="${data && data[field.name] || ''}" ${field.required ? 'required' : ''}>
                </div>
            `;
        }).join('');
    }

    // 处理表单提交
    handleFormSubmit(rowId, modal) {
        document.getElementById('save-edit').addEventListener('click', async () => {
            const form = document.getElementById('editForm');
            const formData = new FormData(form);
            
            try {
                // 逐个更新字段
                for (let [field, value] of formData.entries()) {
                    await this.apiService.updateData(rowId, field, value);
                }
                
                this.showToast('更新成功', 'success');
                modal.hide();
                this.initialize(); // 重新加载数据
            } catch (error) {
                this.showError('更新失败：' + error.message);
            }
        });

        // 模态框关闭时清理
        document.getElementById('editModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    // 处理删除操作
    handleDelete(id) {
        this.showPasswordPrompt(async () => {
            try {
                await this.apiService.deleteData(id);
                this.showToast('删除成功', 'success');
                this.initialize(); // 重新加载数据
            } catch (error) {
                this.showError('删除失败：' + error.message);
            }
        });
    }

    async showDetailModal(id) {
        try {
            // 如果已有模态窗，先关闭并移除
            if (this.currentModal) {
                this.currentModal.hide();
                const oldModal = document.getElementById('detailModal');
                if (oldModal) {
                    oldModal.remove();
                }
                this.currentModal = null;
            }

            // 获取详情数据
            const response = await fetch(`/api/users/${id}`);
            const data = await response.json();

            if (data.status === 'success') {
                // 创建模态窗
                const modalHtml = `
                    <div class="modal fade" id="detailModal" tabindex="-1">
                        <div class="modal-dialog modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <h5 class="modal-title">人员详情</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div id="modal-toolbar" class="mb-3">
                                        <!-- 工具栏将通过JS动态添加 -->
                                    </div>
                                    <div class="detail-content">
                                        ${this.generateDetailContent(data.data)}
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                `;

                // 创建并添加模态窗
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = modalHtml;
                const modalElement = tempDiv.firstElementChild;
                document.body.appendChild(modalElement);

                // 初始化工具栏
                this.initializeModalToolbar(modalElement);

                // 初始化模态窗
                this.currentModal = new bootstrap.Modal(modalElement);

                // 绑定模态窗关闭事件
                modalElement.addEventListener('hidden.bs.modal', () => {
                    modalElement.remove();
                    this.currentModal = null;
                });

                // 显示模态窗
                this.currentModal.show();
            }
        } catch (error) {
            console.error('显示详情失败:', error);
            this.showError('获取详情失败: ' + error.message);
        }
    }

    initializeModalToolbar(modalElement) {
        const toolbar = modalElement.querySelector('#modal-toolbar');
        if (!toolbar) return;

        // 清空工具栏
        toolbar.innerHTML = '';

        // 创建新增按钮
        const addButton = document.createElement('button');
        addButton.type = 'button';
        addButton.className = 'btn btn-success btn-sm';
        addButton.innerHTML = '<i class="fas fa-plus"></i> 新增';
        addButton.onclick = () => this.handleAdd();

        // 添加按钮到工具栏
        toolbar.appendChild(addButton);
    }

    generateDetailContent(data) {
        // 生成详情内容的HTML
        let html = '<div class="table-responsive"><table class="table table-bordered">';
        for (const [key, value] of Object.entries(data)) {
            html += `
                <tr>
                    <th width="30%">${key}</th>
                    <td>${value || '-'}</td>
                </tr>
            `;
        }
        html += '</table></div>';
        return html;
    }
} 
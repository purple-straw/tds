export class UIController {
    constructor() {
        this.elements = {
            totalCard: '#total-card',
            rankCard: '#rank-card',
            totalComparison: '#total-comparison',
            rankComparison: '#rank-comparison',
            showTotal: '#show-total',
            showRank: '#show-rank',
            apiTotalStat: '#api-total-stat',
            dbTotalStat: '#db-total-stat',
            matchRateStat: '#match-rate-stat',
            seriesFilter: '#series-filter',
            modal: '#dbDataModal',
            tableHeaders: '#table-headers',
            tableBody: '#table-body',
            modalTitle: '.modal-title',
            iframeContainer: '#iframe-container',
            tableContainer: '#table-container',
            externalPage: '#external-page'
        };
    }

    getElement(selector) {
        const element = document.querySelector(selector);
        console.log(`Getting element with selector: ${selector}`, element);
        return element;
    }

    updateVisibility() {
        console.log('更新显示状态...');
        const showTotal = this.getElement(this.elements.showTotal).checked;
        const showRank = this.getElement(this.elements.showRank).checked;
        
        const totalCard = this.getElement(this.elements.totalCard);
        const rankCard = this.getElement(this.elements.rankCard);
        
        if (totalCard) {
            totalCard.style.display = showTotal ? 'block' : 'none';
            console.log('Total card visibility:', showTotal);
        }
        
        if (rankCard) {
            rankCard.style.display = showRank ? 'block' : 'none';
            console.log('Rank card visibility:', showRank);
        }

        // 获取最后一次更新的数据
        const lastData = this._lastData;
        if (lastData) {
            // 更新匹配率统计
            this.updateStatsPanel(lastData);
        }
    }

    updateTotalComparison(data) {
        const container = this.getElement(this.elements.totalComparison);
        if (!container) return;
        
        if (data.error) {
            container.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            return;
        }
        
        // 保存最后一次更新的数据，用于显示控制时重新计算匹配率
        this._lastData = data;
        
        container.innerHTML = this.generateTotalComparisonHTML(data);
        this.updateStatsPanel(data);
    }

    // 添加一个计算颜色的方法
    getMatchRateColor(rate) {
        if (rate === 100) {
            return '#28a745';  // 绿色
        } else {
            // 使用 HSL 颜色空间来实现更好的渐变效果
            // hue: 0 是红色
            // saturation: 保持在 70%
            // lightness: 根据匹配率调整亮度，匹配率越低越深
            const hue = 0;  // 红色
            const saturation = 70;  // 70% 饱和度
            const lightness = 30 + (rate / 100) * 40;  // 亮度从 30% 到 70%
            return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
        }
    }

    updateStatsPanel(data) {
        if (data.error) return;
        
        // 显示组织分析详情链接
        const apiTotalStat = this.getElement(this.elements.apiTotalStat);
        apiTotalStat.innerHTML = `<a href="#" style="color: inherit; text-decoration: none;">查看详情</a>`;
        
        // 显示数据库人员信息链接
        const dbTotalStat = this.getElement(this.elements.dbTotalStat);
        dbTotalStat.innerHTML = `<a href="#" style="color: inherit; text-decoration: none;">查看详情</a>`;
        
        // 获取当前显示的项目
        const showTotal = this.getElement(this.elements.showTotal).checked;
        const showRank = this.getElement(this.elements.showRank).checked;
        
        let totalItems = 0;  // 总对比项数
        let matchedItems = 0;  // 匹配项数
        
        // 如果显示总人数和平均年龄对比
        if (showTotal) {
            totalItems += 2;  // 总人数和平均年龄两项
            
            // 检查总人数是否匹配
            if (data.matched) {
                matchedItems++;
            }
            
            // 检查平均年龄是否匹配
            if (data.age_matched) {
                matchedItems++;
            }
        }
        
        // 如果显示职级分布对比
        if (showRank && data.rank_data) {
            const rankComparison = data.rank_data.comparison || {};
            const series = ['P序列', 'M序列', 'B序列'];
            
            // 遍历每个序列
            series.forEach(s => {
                if (data.rank_data.api_data[s]) {
                    const levels = Object.keys(data.rank_data.api_data[s]);
                    totalItems += levels.length;  // 每个职级算一项
                    
                    // 检查每个职级是否匹配
                    levels.forEach(level => {
                        if (!rankComparison[s] || !rankComparison[s][level]) {
                            matchedItems++;  // 如果在comparison中没有出现，说明匹配
                        }
                    });
                }
            });
        }
        
        // 计算匹配率
        const matchRate = totalItems > 0 ? Math.round((matchedItems / totalItems) * 100) : 0;
        
        // 获取颜色
        const color = this.getMatchRateColor(matchRate);
        
        // 显示匹配率
        const matchRateStat = this.getElement(this.elements.matchRateStat);
        if (matchRateStat) {
            matchRateStat.innerHTML = `
                <div class="d-flex align-items-center">
                    <span class="me-2" style="
                        color: ${color};
                        font-weight: bold;
                        font-size: 1.2em;
                        text-shadow: 0 0 1px rgba(0,0,0,0.1);
                        transition: all 0.3s ease;
                    ">${matchRate}%</span>
                    <small class="text-muted">(${matchedItems}/${totalItems}项匹配)</small>
                </div>
            `;
        }
    }

    generateTotalComparisonHTML(data) {
        return `
            <div class="table-responsive">
                <table class="table table-bordered table-hover comparison-table">
                    <thead>
                        <tr>
                            <th>对比项</th>
                            <th>API数据</th>
                            <th>数据库数据</th>
                            <th>差异</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- 总人数对比 -->
                        <tr class="table-secondary">
                            <td colspan="4"><strong>总人数</strong></td>
                        </tr>
                        <tr class="${data.matched ? '' : 'table-warning'}">
                            <td>总人数</td>
                            <td>${data.api_total}人</td>
                            <td>${data.db_total}人</td>
                            <td>
                                <span class="difference-badge ${data.matched ? 'success' : 'danger'}">
                                    ${data.matched ? '无差异' : `差异: ${Math.abs(data.api_total - data.db_total)}人`}
                                </span>
                            </td>
                        </tr>
                        
                        <!-- 平均年龄对比 -->
                        <tr class="table-secondary">
                            <td colspan="4"><strong>平均年龄</strong></td>
                        </tr>
                        <tr class="${data.age_matched ? '' : 'table-warning'}">
                            <td>平均年龄</td>
                            <td>${data.api_avg_age}岁</td>
                            <td>${data.db_avg_age}岁</td>
                            <td>
                                <span class="difference-badge ${data.age_matched ? 'success' : 'danger'}">
                                    ${data.age_matched ? '无差异' : `差异: ${data.difference}岁`}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        `;
    }

    showLoadingSpinner(container) {
        if (!container) return;
        
        container.innerHTML = `
            <div class="d-flex justify-content-center my-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
    }

    showModal(title) {
        const modalElement = this.getElement(this.elements.modal);
        
        // 确保移除可能存在的旧遮罩
        const backdrop = document.querySelector('.modal-backdrop');
        if (backdrop) {
            backdrop.remove();
        }
        document.body.classList.remove('modal-open');
        
        const modal = new bootstrap.Modal(modalElement, {
            backdrop: 'static',
            keyboard: false
        });
        
        // 确保表格容器可见
        this.getElement(this.elements.iframeContainer).style.display = 'none';
        this.getElement(this.elements.tableContainer).style.display = 'block';
        
        // 设置标题
        const titleElement = this.getElement(this.elements.modalTitle);
        titleElement.innerHTML = title;

        // 添加新增按钮（如果不存在且不是组织分析详情页面）
        const modalHeader = modalElement.querySelector('.modal-header');
        const isOrganizationAnalysis = title.includes('组织分析详情');
        
        // 先移除已存在的新增按钮（如果有）
        const existingAddBtn = modalHeader.querySelector('.add-btn');
        if (existingAddBtn) {
            existingAddBtn.remove();
        }
        
        // 如果不是组织分析详情页面，则添加新增按钮
        if (modalHeader && !isOrganizationAnalysis) {
            const addButton = document.createElement('button');
            addButton.className = 'btn btn-success btn-sm ms-auto me-2 add-btn';
            addButton.innerHTML = '<i class="fas fa-plus"></i> 新增';
            addButton.onclick = () => this.showAddForm();
            
            // 将按钮插入到关闭按钮之前
            const closeButton = modalHeader.querySelector('.btn-close');
            modalHeader.insertBefore(addButton, closeButton);
        }
        
        // 添加关闭事件监听器
        modalElement.addEventListener('hidden.bs.modal', () => {
            // 移除模态窗口的遮罩和相关类
            const backdrop = document.querySelector('.modal-backdrop');
            if (backdrop) {
                backdrop.remove();
            }
            document.body.classList.remove('modal-open');
            document.body.style.overflow = '';
            document.body.style.paddingRight = '';
        });
        
        modal.show();
        return modal;
    }

    updateModalContent(data) {
        const tableHeaders = this.getElement(this.elements.tableHeaders);
        const tableBody = this.getElement(this.elements.tableBody);
        
        if (data.error) {
            tableBody.innerHTML = `<tr><td colspan="100%" class="text-danger">加载失败: ${data.error}</td></tr>`;
            return;
        }
        
        if (!data.data || !data.data.length) {
            tableBody.innerHTML = '<tr><td colspan="100%" class="text-center">暂无数据</td></tr>';
            return;
        }
        
        // 生成表头
        const headers = Object.keys(data.data[0]);
        tableHeaders.innerHTML = headers.map(header => 
            `<th scope="col" data-field="${header}">${header}</th>`
        ).join('');
        
        // 生成表体
        tableBody.innerHTML = data.data.map(row => `
            <tr>
                ${headers.map(header => 
                    `<td data-field="${header}" title="${row[header] || ''}">${row[header] || ''}</td>`
                ).join('')}
            </tr>
        `).join('');
    }

    updateRankComparison(data, selectedSeries = 'P序列') {
        console.log('Updating rank comparison with data:', data);
        console.log('Selected series:', selectedSeries);
        
        const container = this.getElement(this.elements.rankComparison);
        if (!container) return;
        
        if (!data || !data.data) {
            container.innerHTML = `<div class="alert alert-danger">暂无数据</div>`;
            return;
        }
        
        // 确保我们有正确的数据结构
        const apiData = data.data?.api_data || {};
        const dbData = data.data?.db_data || {};
        const comparison = data.data?.comparison || {};
        
        console.log('API Data:', apiData);
        console.log('DB Data:', dbData);
        console.log('Comparison:', comparison);
        
        // 创建表格HTML
        let html = `
            <div class="table-responsive">
                <table class="table table-bordered table-hover comparison-table">
                    <thead>
                        <tr>
                            <th>职级</th>
                            <th>API数据</th>
                            <th>数据库数据</th>
                            <th>差异</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        // 处理选中的序列
        const seriesToShow = selectedSeries === 'all' ? ['P序列', 'M序列', 'B序列'] : [selectedSeries];
        console.log('Series to show:', seriesToShow);
        
        // 遍历每个序列
        seriesToShow.forEach(series => {
            // 添加序列标题行
            html += `
                <tr class="table-secondary">
                    <td colspan="4"><strong>${series}</strong></td>
                </tr>
            `;
            
            // 获取当前序列的所有职级
            const apiLevels = apiData[series] || {};
            const dbLevels = dbData[series] || {};
            console.log(`${series} API Levels:`, apiLevels);
            console.log(`${series} DB Levels:`, dbLevels);
            
            // 获取所有唯一的职级
            const allLevels = new Set([...Object.keys(apiLevels), ...Object.keys(dbLevels)]);
            const sortedLevels = [...allLevels].sort();
            console.log(`${series} All Levels:`, sortedLevels);
            
            if (sortedLevels.length === 0) {
                html += `
                    <tr>
                        <td colspan="4" class="text-center">暂无数据</td>
                    </tr>
                `;
            } else {
                // 遍历所有职级
                sortedLevels.forEach(level => {
                    const apiCount = apiLevels[level] || 0;
                    const dbCount = dbLevels[level] || 0;
                    const isDifferent = apiCount !== dbCount;
                    
                    html += `
                        <tr class="${isDifferent ? 'table-warning' : ''}" data-series="${series}" data-level="${level}">
                            <td>${level}</td>
                            <td class="clickable" data-type="api" data-count="${apiCount}">${apiCount}人</td>
                            <td class="clickable" data-type="db" data-count="${dbCount}">${dbCount}人</td>
                            <td>
                                <span class="difference-badge ${isDifferent ? 'danger' : 'success'}">
                                    ${isDifferent ? `差异: ${Math.abs(apiCount - dbCount)}人` : '无差异'}
                                </span>
                            </td>
                        </tr>
                    `;
                });
            }
        });
        
        html += `
                    </tbody>
                </table>
            </div>
        `;
        
        container.innerHTML = html;

        // 添加点击事件处理
        container.querySelectorAll('.clickable').forEach(cell => {
            cell.style.cursor = 'pointer';
            cell.addEventListener('click', async () => {
                const row = cell.closest('tr');
                const series = row.dataset.series;
                const level = row.dataset.level;
                const type = cell.dataset.type;
                const count = cell.dataset.count;

                // 显示加载中的模态窗
                const modal = this.showModal(`
                    <i class="fas fa-users me-2"></i>
                    ${series} - ${level} 人员详情 (${type === 'api' ? 'API数据' : '数据库数据'})
                    <div class="query-time ms-3">
                        <small class="text-muted">
                            <i class="fas fa-users me-1"></i>共 ${count} 人
                        </small>
                    </div>
                `);

                try {
                    // 根据类型获取不同的数据
                    const data = type === 'api' ? 
                        await this.getApiPersonnelData(series, level) :
                        await this.getDbPersonnelData(series, level);
                    
                    this.displayTableData(data);
                } catch (error) {
                    console.error('加载人员数据失败:', error);
                    this.showError('加载数据失败: ' + error.message);
                }
            });
        });
    }

    async getApiPersonnelData(series, level) {
        try {
            const response = await fetch(`/api/personnel/api?series=${encodeURIComponent(series)}&level=${encodeURIComponent(level)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('获取API人员数据失败');
            }

            const result = await response.json();
            return result.data || [];
        } catch (error) {
            console.error('获取API人员数据失败:', error);
            throw error;
        }
    }

    async getDbPersonnelData(series, level) {
        try {
            const response = await fetch(`/api/personnel/db?series=${encodeURIComponent(series)}&level=${encodeURIComponent(level)}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error('获取数据库人员数据失败');
            }

            const result = await response.json();
            return result.data || [];
        } catch (error) {
            console.error('获取数据库人员数据失败:', error);
            throw error;
        }
    }

    showExternalPage(url) {
        // 先显示模态窗
        const modal = this.showModal('组织画像数据');
        
        // 隐藏表格容器，显示iframe容器
        this.getElement(this.elements.tableContainer).style.display = 'none';
        const iframeContainer = this.getElement(this.elements.iframeContainer);
        iframeContainer.style.display = 'block';
        
        // 设置iframe的src
        const iframe = this.getElement(this.elements.externalPage);
        iframe.src = url;
        
        return modal;
    }

    showTableContainer() {
        this.getElement(this.elements.iframeContainer).style.display = 'none';
        this.getElement(this.elements.tableContainer).style.display = 'block';
    }

    displayTableData(data) {
        console.log('Displaying table data:', data);
        
        const headers = ['ID', '姓名', '职级', '性别', '员工工号', '职位', '入职日期', '状态', '操作'];
        const tableHeaders = document.getElementById('table-headers');
        const tableBody = document.getElementById('table-body');
        
        // 清空现有内容
        tableHeaders.innerHTML = '';
        tableBody.innerHTML = '';
        
        // 添加表头
        headers.forEach(header => {
            const th = document.createElement('th');
            th.textContent = header;
            tableHeaders.appendChild(th);
        });
        
        // 如果没有数据，显示提示信息
        if (!data || !Array.isArray(data) || data.length === 0) {
            console.log('No data to display');
            const tr = document.createElement('tr');
            const td = document.createElement('td');
            td.colSpan = headers.length;
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
                row.id,
                row.name,
                row.level,
                row.gender,
                row.department,
                row.position,
                row.entry_date,
                row.status
            ].forEach((cell, index) => {
                const td = document.createElement('td');
                td.textContent = cell || '-';
                // 添加双击编辑功能
                if (index > 0) { // ID不允许编辑
                    td.addEventListener('dblclick', () => this.makeEditable(td, row.id, headers[index]));
                }
                tr.appendChild(td);
            });

            // 添加操作按钮
            const actionTd = document.createElement('td');
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
                this.showPasswordPrompt(() => this.deleteRecord(rowId));
            });
        });

        // 移除新增按钮（如果当前是组织分析详情页面）
        const modalTitle = this.getElement(this.elements.modalTitle);
        if (modalTitle && modalTitle.textContent.includes('组织分析详情')) {
            const addButton = document.querySelector('.add-btn');
            if (addButton) {
                addButton.remove();
            }
        }
    }

    showAddForm() {
        this.showPasswordPrompt(() => {
            const modalHtml = `
                <div class="modal fade" id="addModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">新增人员</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <form id="addForm">
                                    <div class="mb-3">
                                        <label class="form-label">姓名</label>
                                        <input type="text" class="form-control" name="name" required>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">职级</label>
                                        <input type="text" class="form-control" name="level">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">性别</label>
                                        <select class="form-select" name="gender">
                                            <option value="男">男</option>
                                            <option value="女">女</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">员工工号</label>
                                        <input type="text" class="form-control" name="department">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">职位</label>
                                        <input type="text" class="form-control" name="position">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">入职日期</label>
                                        <input type="date" class="form-control" name="entry_date">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">状态</label>
                                        <select class="form-select" name="status">
                                            <option value="在职">在职</option>
                                            <option value="离职">离职</option>
                                            <option value="试用">试用</option>
                                        </select>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                                <button type="button" class="btn btn-primary" id="saveAdd">保存</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            document.body.insertAdjacentHTML('beforeend', modalHtml);
            const modal = new bootstrap.Modal(document.getElementById('addModal'));
            modal.show();

            document.getElementById('saveAdd').addEventListener('click', () => {
                const formData = new FormData(document.getElementById('addForm'));
                const data = Object.fromEntries(formData.entries());
                this.addRecord(data);
                modal.hide();
            });

            document.getElementById('addModal').addEventListener('hidden.bs.modal', function () {
                this.remove();
            });
        });
    }

    async addRecord(data) {
        try {
            const response = await fetch('/api/db/add', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error('添加失败');
            }

            // 显示成功提示
            this.showToast('添加成功', 'success');
            
            // 刷新数据
            location.reload();
        } catch (error) {
            this.showToast('添加失败: ' + error.message, 'error');
        }
    }

    async deleteRecord(id) {
        if (!confirm('确定要删除这条记录吗？')) {
            return;
        }

        try {
            const response = await fetch('/api/db/delete', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id })
            });

            if (!response.ok) {
                throw new Error('删除失败');
            }

            this.showToast('删除成功', 'success');
            location.reload();
        } catch (error) {
            this.showToast('删除失败: ' + error.message, 'error');
        }
    }

    showToast(message, type = 'success') {
        const toastDiv = document.createElement('div');
        toastDiv.className = 'toast position-fixed top-0 end-0 m-3';
        toastDiv.innerHTML = `
            <div class="toast-header bg-${type} text-white">
                <strong class="me-auto">${type === 'success' ? '成功' : '错误'}</strong>
                <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        `;
        document.body.appendChild(toastDiv);
        
        const toast = new bootstrap.Toast(toastDiv, {
            delay: 3000,
            animation: true
        });
        toast.show();

        setTimeout(() => {
            toastDiv.remove();
        }, 3000);
    }

    makeEditable(td, rowId, field) {
        // 先验证密码
        this.showPasswordPrompt(() => {
            const originalValue = td.textContent;
            td.innerHTML = `
                <input type="text" class="form-control form-control-sm" 
                       value="${originalValue}" 
                       style="width: 100%; min-width: 100px;">
            `;
            const input = td.querySelector('input');
            input.focus();
            
            const saveChanges = async () => {
                const newValue = input.value.trim();
                if (newValue !== originalValue) {
                    try {
                        await this.updateData(rowId, field, newValue);
                        td.textContent = newValue || '-';
                    } catch (error) {
                        // 如果更新失败，恢复原值
                        td.textContent = originalValue;
                    }
                } else {
                    td.textContent = originalValue;
                }
            };
            
            input.addEventListener('blur', saveChanges);
            
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    saveChanges();
                }
            });
        });
    }

    showEditForm(rowId) {
        // 获取当前行数据
        const row = document.querySelector(`[data-id="${rowId}"]`).closest('tr');
        const cells = row.cells;
        
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
                                <div class="mb-3">
                                    <label class="form-label">姓名</label>
                                    <input type="text" class="form-control" name="name" value="${cells[1].textContent}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">职级</label>
                                    <input type="text" class="form-control" name="level" value="${cells[2].textContent}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">性别</label>
                                    <select class="form-select" name="gender">
                                        <option value="男" ${cells[3].textContent === '男' ? 'selected' : ''}>男</option>
                                        <option value="女" ${cells[3].textContent === '女' ? 'selected' : ''}>女</option>
                                    </select>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">部门</label>
                                    <input type="text" class="form-control" name="department" value="${cells[4].textContent}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">职位</label>
                                    <input type="text" class="form-control" name="position" value="${cells[5].textContent}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">入职日期</label>
                                    <input type="date" class="form-control" name="entry_date" value="${cells[6].textContent}">
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">状态</label>
                                    <select class="form-select" name="status">
                                        <option value="在职" ${cells[7].textContent === '在职' ? 'selected' : ''}>在职</option>
                                        <option value="离职" ${cells[7].textContent === '离职' ? 'selected' : ''}>离职</option>
                                        <option value="试用" ${cells[7].textContent === '试用' ? 'selected' : ''}>试用</option>
                                    </select>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                            <button type="button" class="btn btn-primary" id="saveEdit">保存</button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', modalHtml);
        const modal = new bootstrap.Modal(document.getElementById('editModal'));
        modal.show();

        document.getElementById('saveEdit').addEventListener('click', async () => {
            const form = document.getElementById('editForm');
            const formData = new FormData(form);
            
            // 逐个更新字段
            for (let [field, value] of formData.entries()) {
                if (value !== cells[['name', 'level', 'gender', 'department', 'position', 'entry_date', 'status']
                    .indexOf(field) + 1].textContent) {
                    await this.updateData(rowId, field, value);
                }
            }
            
            modal.hide();
            location.reload();  // 刷新页面以显示更新后的数据
        });

        document.getElementById('editModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

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

        // 处理密码确认
        document.getElementById('confirm-password').addEventListener('click', () => {
            const password = document.getElementById('password-input').value;
            if (password === '10086') {
                modal.hide();
                if (callback) callback();
            } else {
                alert('密码错误！');
            }
        });

        // 添加回车键支持
        document.getElementById('password-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                document.getElementById('confirm-password').click();
            }
        });

        // 模态框关闭时清理
        document.getElementById('passwordModal').addEventListener('hidden.bs.modal', function () {
            this.remove();
        });
    }

    async updateData(rowId, field, value) {
        try {
            console.log('Updating data:', { rowId, field, value });  // 添加日志
            const response = await fetch('/api/db/update', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({
                    id: rowId,
                    field: field.toLowerCase(),  // 确保字段名小写
                    value: value
                })
            });

            // 检查响应状态
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            if (result.success) {
                // 显示成功提示
                this.showToast('更新成功', 'success');
                
                // 可选：刷新数据
                // location.reload();
            } else {
                throw new Error(result.error || '更新失败');
            }
        } catch (error) {
            console.error('更新失败:', error);
            this.showToast('更新失败: ' + error.message, 'error');
            throw error;
        }
    }

    showError(message) {
        const container = this.getElement(this.elements.tableContainer);
        container.style.display = 'block';
        container.innerHTML = `
            <div class="alert alert-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                ${message}
            </div>
        `;
        
        // 隐藏iframe容器
        this.getElement(this.elements.iframeContainer).style.display = 'none';
    }
}
export class AppController {
    constructor(dataService, uiController) {
        this.dataService = dataService;
        this.uiController = uiController;
        this.rankData = null;
    }

    init() {
        console.log('页面加载完成，开始初始化...');
        this.bindEvents();
        this.loadInitialData();
    }

    bindEvents() {
        // 监听复选框变化
        document.querySelectorAll('.form-check-input').forEach(checkbox => {
            checkbox.addEventListener('change', () => this.uiController.updateVisibility());
        });
        
        // 为组织分析详情添加点击事件
        const apiTotalStat = this.uiController.getElement('#api-total-stat');
        if (apiTotalStat) {
            apiTotalStat.addEventListener('click', async (e) => {
                e.preventDefault();
                await this.loadApiData();
            });
        }

        // 为数据库人员信息添加点击事件
        const dbTotalStat = this.uiController.getElement('#db-total-stat');
        if (dbTotalStat) {
            dbTotalStat.addEventListener('click', async (e) => {
                e.preventDefault();
                const modal = this.uiController.showModal('数据库人员信息');
                try {
                    const result = await this.dataService.getDbData();
                    if (result.error) {
                        throw new Error(result.error);
                    }
                    this.uiController.displayTableData(result.data);
                } catch (error) {
                    console.error('Error loading DB data:', error);
                }
                
                // 添加模态窗口关闭事件处理
                const modalElement = this.uiController.getElement('#dbDataModal');
                modalElement.addEventListener('hidden.bs.modal', () => {
                    // 确保页面恢复正常状态
                    document.body.classList.remove('modal-open');
                    document.body.style.overflow = '';
                    document.body.style.paddingRight = '';
                    const backdrop = document.querySelector('.modal-backdrop');
                    if (backdrop) {
                        backdrop.remove();
                    }
                });
            });
        }
        
        // 监听序列筛选
        const seriesFilter = this.uiController.getElement(this.uiController.elements.seriesFilter);
        console.log('Series filter element:', seriesFilter);
        if (seriesFilter) {
            console.log('Adding change event listener to series filter');
            seriesFilter.addEventListener('change', (e) => {
                console.log('Series filter changed:', e.target.value);
                this.displayRankData(e.target.value);
            });
        } else {
            console.warn('Series filter element not found!');
        }
    }

    async loadInitialData() {
        try {
            // 显示加载状态
            this.uiController.showLoadingSpinner(
                this.uiController.getElement(this.uiController.elements.totalComparison)
            );

            // 并行加载所有数据
            const [totalResult, ageResult, rankResult] = await Promise.all([
                this.dataService.getTotalComparison(),
                this.dataService.getAgeComparison(),
                this.dataService.getRankComparison()
            ]);

            console.log('Rank result in loadInitialData:', rankResult);

            // 保存职级数据用于后续筛选
            this.rankData = rankResult;

            // 合并数据，确保正确处理数字类型
            const combinedData = {
                api_total: parseInt(totalResult.data.api_total) || 0,
                db_total: parseInt(totalResult.data.db_total) || 0,
                matched: totalResult.data.matched,
                api_avg_age: parseFloat(ageResult.data.api_avg_age) || 0,
                db_avg_age: parseFloat(ageResult.data.db_avg_age) || 0,
                difference: parseFloat(ageResult.data.difference) || 0,
                age_matched: Math.abs(parseFloat(ageResult.data.api_avg_age) - parseFloat(ageResult.data.db_avg_age)) <= 0.1,
                rank_data: {
                    api_data: rankResult.data?.api_data || {},  // 确保数据结构正确
                    db_data: rankResult.data?.db_data || {},
                    comparison: rankResult.data?.comparison || {}
                }
            };
            
            // 更新UI显示
            this.uiController.updateTotalComparison(combinedData);
            
            // 更新职级分布显示
            this.uiController.updateRankComparison(rankResult, 'P序列'); // 默认显示P序列
            
        } catch (error) {
            console.error('加载数据失败:', error);
            this.uiController.showError('加载数据失败: ' + error.message);
        }
    }

    async loadRankData() {
        try {
            const data = await this.dataService.getRankComparison();
            this.rankData = data;
            this.uiController.updateRankComparison(data);
            return data;  // 返回数据
        } catch (error) {
            console.error('加载职级分布数据失败:', error);
            this.uiController.updateRankComparison({ error: '加载数据失败' });
            return null;
        }
    }

    displayRankData(series) {
        console.log('Displaying rank data for series:', series);
        console.log('Current rank data:', this.rankData);
        if (this.rankData && this.rankData.data) {  // 确保有 data 属性
            this.uiController.updateRankComparison(this.rankData, series);
        } else {
            console.warn('No rank data available');
            // 如果没有数据，重新加载
            this.loadRankData().then(data => {
                if (data && data.data) {  // 确保有 data 属性
                    this.uiController.updateRankComparison(data, series);
                }
            });
        }
    }

    async loadDbTableData() {
        const modal = this.uiController.showModal(`
            <i class="fas fa-database me-2"></i>
            数据库表数据 (per_main)
        `);
        
        // 确保显示表格容器
        this.uiController.showTableContainer();
        
        try {
            const data = await this.dataService.getDbData();
            if (data.data && data.data.length > 0) {
                // 定义字段顺序
                const preferredOrder = [
                    'name',      // 姓名
                    'id',        // ID
                    'level',     // 职级
                    'gender',    // 性别
                ];
                
                // 重新排序数据中的字段
                const formattedData = {
                    data: data.data.map(row => {
                        const orderedRow = {};
                        // 先添加优先字段
                        preferredOrder.forEach(field => {
                            if (field in row) {
                                orderedRow[field] = row[field];
                            }
                        });
                        // 再添加其他字段
                        Object.keys(row).forEach(field => {
                            if (!preferredOrder.includes(field)) {
                                orderedRow[field] = row[field];
                            }
                        });
                        return orderedRow;
                    })
                };
                
                this.uiController.updateModalContent(formattedData);
            } else {
                this.uiController.updateModalContent(data);
            }
        } catch (error) {
            console.error('加载数据库数据失败:', error);
            this.uiController.updateModalContent({ error: '加载数据失败' });
        }
    }

    async loadApiData() {
        const modal = this.uiController.showModal(`
            <i class="fas fa-sitemap me-2"></i>
            组织分析详情
            <div class="query-time ms-3">
                <small class="text-muted">
                    <i class="fas fa-clock me-1"></i>查询耗时：<span id="query-time">0</span> ms
                </small>
            </div>
        `);
        
        try {
            const data = await this.dataService.getApiData();
            if (data.data && data.data.length > 0) {
                this.uiController.displayTableData(data.data);
            } else {
                this.uiController.updateModalContent(data);
            }
        } catch (error) {
            console.error('加载组织分析数据失败:', error);
            this.uiController.showError('加载数据失败: ' + error.message);
        }
    }
} 
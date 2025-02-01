import { BaseController } from './BaseController.js';
import { ApiService } from '../services/ApiService.js';

export class ComparisonController extends BaseController {
    constructor() {
        super();
        this.apiService = new ApiService();
        this.elements = {
            totalComparison: '#total-comparison',
            rankComparison: '#rank-comparison',
            seriesFilter: '#series-filter',
            matchRateStat: '#match-rate-stat',
            apiTotalStat: '#api-total-stat',
            dbTotalStat: '#db-total-stat'
        };
        
        this.initialize();
        this.bindEvents();
    }

    // 初始化
    async initialize() {
        await Promise.all([
            this.updateTotalComparison(),
            this.updateRankComparison()
        ]);
    }

    // 绑定事件
    bindEvents() {
        const seriesFilter = this.getElement(this.elements.seriesFilter);
        if (seriesFilter) {
            seriesFilter.addEventListener('change', () => {
                this.updateRankComparison(seriesFilter.value);
            });
        }
    }

    // 更新总人数对比
    async updateTotalComparison() {
        try {
            const container = this.getElement(this.elements.totalComparison);
            this.showLoading(container);

            const result = await this.apiService.getTotalComparison();
            if (!result || !result.data) {
                throw new Error('获取数据失败');
            }

            const { api_count, db_count, match_rate } = result.data;
            
            // 更新统计数据
            this.updateStats(api_count, db_count, match_rate);
            
            // 生成对比图表
            this.renderTotalChart(container, api_count, db_count);
            
        } catch (error) {
            this.showError('更新总人数对比失败：' + error.message);
        }
    }

    // 更新职级分布对比
    async updateRankComparison(selectedSeries = 'P序列') {
        try {
            const container = this.getElement(this.elements.rankComparison);
            this.showLoading(container);

            const result = await this.apiService.getRankComparison();
            if (!result || !result.data) {
                throw new Error('获取数据失败');
            }

            const { api_data, db_data, comparison } = result.data;
            this.renderRankComparison(container, api_data, db_data, comparison, selectedSeries);
            
        } catch (error) {
            this.showError('更新职级分布对比失败：' + error.message);
        }
    }

    // 更新统计数据
    updateStats(apiCount, dbCount, matchRate) {
        const apiTotalStat = this.getElement(this.elements.apiTotalStat);
        const dbTotalStat = this.getElement(this.elements.dbTotalStat);
        const matchRateStat = this.getElement(this.elements.matchRateStat);

        if (apiTotalStat) apiTotalStat.textContent = `${apiCount}人`;
        if (dbTotalStat) dbTotalStat.textContent = `${dbCount}人`;
        
        if (matchRateStat) {
            matchRateStat.textContent = `${(matchRate * 100).toFixed(1)}%`;
            // 根据匹配率设置颜色
            matchRateStat.className = 'match-rate ' + this.getMatchRateClass(matchRate);
        }
    }

    // 获取匹配率对应的样式类
    getMatchRateClass(rate) {
        if (rate >= 0.9) return 'high';
        if (rate >= 0.7) return 'medium';
        return 'low';
    }

    // 渲染总人数对比图表
    renderTotalChart(container, apiCount, dbCount) {
        container.innerHTML = `
            <div class="comparison-chart">
                <div class="chart-item">
                    <div class="chart-label">API数据</div>
                    <div class="chart-value">${apiCount}人</div>
                    <div class="chart-bar" style="width: ${(apiCount / Math.max(apiCount, dbCount) * 100)}%"></div>
                </div>
                <div class="chart-item">
                    <div class="chart-label">数据库数据</div>
                    <div class="chart-value">${dbCount}人</div>
                    <div class="chart-bar" style="width: ${(dbCount / Math.max(apiCount, dbCount) * 100)}%"></div>
                </div>
            </div>
        `;
    }

    // 渲染职级分布对比
    renderRankComparison(container, apiData, dbData, comparison, selectedSeries) {
        const seriesToShow = selectedSeries === 'all' ? ['P序列', 'M序列', 'B序列'] : [selectedSeries];
        
        let html = `
            <div class="table-responsive">
                <table class="table table-bordered comparison-table">
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

        seriesToShow.forEach(series => {
            // 添加序列标题行
            html += `
                <tr class="table-secondary">
                    <td colspan="4"><strong>${series}</strong></td>
                </tr>
            `;
            
            const apiLevels = apiData[series] || {};
            const dbLevels = dbData[series] || {};
            const allLevels = new Set([...Object.keys(apiLevels), ...Object.keys(dbLevels)]);
            const sortedLevels = [...allLevels].sort();

            if (sortedLevels.length === 0) {
                html += `
                    <tr>
                        <td colspan="4" class="text-center">暂无数据</td>
                    </tr>
                `;
            } else {
                sortedLevels.forEach(level => {
                    const apiCount = apiLevels[level] || 0;
                    const dbCount = dbLevels[level] || 0;
                    const isDifferent = apiCount !== dbCount;
                    
                    html += `
                        <tr class="${isDifferent ? 'table-warning' : ''}">
                            <td>${level}</td>
                            <td>${apiCount}人</td>
                            <td>${dbCount}人</td>
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
    }
} 
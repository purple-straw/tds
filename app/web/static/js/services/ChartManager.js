import { chartConfig } from '../utils/chartUtils.js';

export class ChartManager {
    constructor() {
        this.charts = new Map();
        this.resizeHandler = this.handleResize.bind(this);
        window.addEventListener('resize', this.resizeHandler);
    }

    init(containerId, type) {
        const container = document.getElementById(containerId);
        if (!container) return null;

        const chart = echarts.init(container);
        const config = type === 'total' ? chartConfig.totalChart : chartConfig.rankChart;
        chart.setOption(config);
        this.charts.set(containerId, chart);
        return chart;
    }

    getChart(containerId) {
        return this.charts.get(containerId);
    }

    updateChart(containerId, data) {
        const chart = this.getChart(containerId);
        if (chart) {
            chart.setOption(data);
        }
    }

    handleResize() {
        this.charts.forEach(chart => chart.resize());
    }

    dispose() {
        this.charts.forEach(chart => chart.dispose());
        this.charts.clear();
        window.removeEventListener('resize', this.resizeHandler);
    }
} 
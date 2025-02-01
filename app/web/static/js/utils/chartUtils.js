// 图表配置
export const chartConfig = {
    totalChart: {
        title: {
            text: '总人数对比',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        legend: {
            top: 30,
            data: ['API数据', '数据库数据']
        },
        grid: {
            top: 80,
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['P序列', 'M序列', 'B序列']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'API数据',
                type: 'bar',
                data: [120, 200, 150],
                itemStyle: {
                    color: '#409EFF'
                }
            },
            {
                name: '数据库数据',
                type: 'bar',
                data: [130, 190, 145],
                itemStyle: {
                    color: '#67C23A'
                }
            }
        ]
    },
    rankChart: {
        title: {
            text: '职级分布对比',
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        legend: {
            top: 30,
            data: ['API数据', '数据库数据']
        },
        grid: {
            top: 80,
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            data: ['P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8']
        },
        yAxis: {
            type: 'value'
        },
        series: [
            {
                name: 'API数据',
                type: 'line',
                smooth: true,
                data: [10, 30, 50, 80, 70, 40, 20, 10],
                itemStyle: {
                    color: '#409EFF'
                },
                lineStyle: {
                    width: 3
                },
                symbolSize: 8
            },
            {
                name: '数据库数据',
                type: 'line',
                smooth: true,
                data: [12, 32, 48, 78, 73, 38, 22, 8],
                itemStyle: {
                    color: '#67C23A'
                },
                lineStyle: {
                    width: 3
                },
                symbolSize: 8
            }
        ]
    }
}; 
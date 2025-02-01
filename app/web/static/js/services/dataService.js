class DataService {
    constructor() {
        this.BASE_URL = 'https://test-tds-standard.cepin.com';
    }

    async getTotalComparison() {
        try {
            const response = await fetch('/api/comparison/total');
            const result = await response.json();
            console.log('Total comparison result:', result); // 添加调试日志
            if (result.error) {
                throw new Error(result.error);
            }
            return result;  // 返回完整的响应
        } catch (error) {
            console.error('Error fetching total comparison:', error);
            throw error;
        }
    }
    
    async getRankComparison() {
        try {
            const response = await fetch('/api/comparison/rank');
            const result = await response.json();
            console.log('Rank comparison raw result:', result); // 添加调试日志
            
            if (result.error) {
                throw new Error(result.error);
            }
            
            // 确保返回正确的数据结构
            return {
                data: {
                    api_data: result.data?.api_data || {},
                    db_data: result.data?.db_data || {},
                    comparison: result.data?.comparison || {}
                }
            };
        } catch (error) {
            console.error('Error fetching rank comparison:', error);
            throw error;
        }
    }
    
    async getDbData() {
        try {
            console.log('Fetching DB data...'); // 添加调试日志
            const response = await fetch('/api/db/data');
            const result = await response.json();
            console.log('DB data received:', result); // 添加调试日志
            
            // 更新查询时间显示
            const queryTimeElement = document.getElementById('query-time');
            if (result.query_time) {
                queryTimeElement.textContent = result.query_time;
            }
            
            if (result.error) {
                throw new Error(result.error);
            }
            
            return result;
        } catch (error) {
            console.error('Error fetching DB data:', error);
            throw error;
        }
    }
    
    async getApiData() {
        try {
            const response = await fetch('/api/api-data');
            const result = await response.json();
            return result.data || result;
        } catch (error) {
            console.error('Error fetching API data:', error);
            throw error;
        }
    }

    async fetchTableData(type) {
        try {
            const response = await fetch(`/api/data/${type}`);
            const result = await response.json();
            
            // 更新查询时间显示
            const queryTimeElement = document.getElementById('query-time');
            if (result.query_time) {
                queryTimeElement.textContent = result.query_time;
            }
            
            // 返回实际的数据部分
            return result.data;
        } catch (error) {
            console.error('Error fetching table data:', error);
            throw error;
        }
    }

    async loadApiData() {
        try {
            const startTime = performance.now();
            const url = `${this.BASE_URL}/#/tissue-analysis/portrait`;
            
            // 创建一个Promise来处理页面加载
            const loadPromise = new Promise((resolve, reject) => {
                const iframe = document.getElementById('external-page');
                
                iframe.onload = () => {
                    const endTime = performance.now();
                    const loadTime = Math.round(endTime - startTime);
                    resolve(loadTime);
                };
                
                iframe.onerror = () => {
                    reject(new Error('页面加载失败'));
                };
                
                // 设置超时
                setTimeout(() => {
                    reject(new Error('页面加载超时'));
                }, 30000); // 30秒超时
            });
            
            return {
                url: url,
                loadTime: await loadPromise
            };
        } catch (error) {
            console.error('Error loading API page:', error);
            throw error;
        }
    }

    async getAgeComparison() {
        try {
            const response = await fetch('/api/comparison/age');
            const result = await response.json();
            console.log('Age comparison result:', result); // 添加调试日志
            if (result.error) {
                throw new Error(result.error);
            }
            return result;  // 返回完整的响应
        } catch (error) {
            console.error('获取平均年龄对比数据失败:', error);
            throw error;
        }
    }
}

export { DataService }; 
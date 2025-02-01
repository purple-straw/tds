export class ApiService {
    constructor() {
        this.baseUrl = '';
    }

    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Get Error:', error);
            throw error;
        }
    }

    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API Post Error:', error);
            throw error;
        }
    }

    // API端点方法
    async getTotalComparison() {
        return this.get('/api/comparison/total');
    }

    async getRankComparison() {
        return this.get('/api/comparison/rank');
    }

    async getDbData() {
        return this.get('/api/db/data');
    }

    async getApiData() {
        return this.get('/api/api-data');
    }

    async updateData(id, field, value) {
        return this.post('/api/db/update', { id, field, value });
    }

    async addData(data) {
        return this.post('/api/db/add', data);
    }

    async deleteData(id) {
        return this.post('/api/db/delete', { id });
    }
} 
// 导入模块
import { DataService } from './services/dataService.js';
import { UIController } from './controllers/uiController.js';
import { AppController } from './controllers/appController.js';

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    const app = new AppController(new DataService(), new UIController());
    app.init();
});

// 在显示模态框数据的函数中添加时间显示
function showModalData(data) {
    // ... 原有的表格显示代码 ...
    
    // 更新查询时间显示
    const queryTimeElement = document.getElementById('query-time');
    if (data.query_time) {
        queryTimeElement.textContent = data.query_time;
    } else {
        queryTimeElement.textContent = '0';
    }
} 
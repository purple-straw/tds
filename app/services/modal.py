from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ModalButton:
    id: str
    text: str
    icon: str = ""
    class_name: str = "btn-primary"
    on_click: str = ""

class ModalService:
    def create_detail_modal(self, data: Dict[str, Any]) -> str:
        """创建详情模态窗HTML"""
        return f"""
            <div class="modal fade" id="detailModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title">人员详情</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="detail-content">
                                <!-- 工具栏 -->
                                <div class="toolbar mb-3" id="modal-toolbar">
                                    <!-- 工具栏内容由JS动态生成 -->
                                </div>
                                <!-- 详情表格 -->
                                <div class="table-responsive">
                                    {self._generate_detail_table(data)}
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                        </div>
                    </div>
                </div>
            </div>
        """

    def _generate_detail_table(self, data: Dict[str, Any]) -> str:
        """生成详情表格HTML"""
        rows = []
        for key, value in data.items():
            rows.append(f"""
                <tr>
                    <th width="30%">{key}</th>
                    <td>{value or '-'}</td>
                </tr>
            """)
        
        return f"""
            <table class="table table-bordered">
                <tbody>
                    {''.join(rows)}
                </tbody>
            </table>
        """

    def _get_detail_buttons(self) -> List[ModalButton]:
        """获取详情模态窗按钮配置"""
        return [
            ModalButton(
                id="close-modal",
                text="关闭",
                class_name="btn-secondary",
                on_click="modal.hide()"
            )
        ]

modal_service = ModalService() 
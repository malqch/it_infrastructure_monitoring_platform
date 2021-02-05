<template>
    <div>
        <div class="wrapper">
            <!--<div class="crumbs">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>
                        <i class="el-icon-lx-cascades"></i> 告警策略管理
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div>-->
            <div class="container">
                <el-form :inline="true" v-model="form">
                    <el-row type="flex" class="row-bg" justify="space-between">
<!--                        <div>-->
<!--                            <el-button-->
<!--                                    type="primary"-->
<!--                                    icon="el-icon-edit"-->
<!--                                    @click="handleCreate()"-->
<!--                                    class="handle-box-1"-->
<!--                            >增加-->
<!--                            </el-button>-->
<!--                        </div>-->
<!--                        <div type="flex" class="row-bg" justify="end">-->
<!--                            <el-form-item>-->
<!--                                <el-input v-model="searchData.strategy_name" clearable placeholder="告警等级名称" class="handle-input"></el-input>-->
<!--                            </el-form-item>-->
<!--                            <el-button icon="el-icon-search" type="primary" class="handle-box change_el_button" @click="handleSearch">查询</el-button>-->
<!--                        </div>-->
                    </el-row>
                </el-form>
                <el-table
                        :data="tableData"
                        border
                        ref="multipleTable"
                        header-cell-class-name="table-header"
                        @selection-change="handleSelectionChange"
                >
                    <el-table-column width="50px" type="index" label="序号" align="center"></el-table-column>
                    <el-table-column prop="strategy_name" label="告警策略名称" align="center"></el-table-column>
                    <el-table-column prop="strategy_level" label="告警策略等级" align="center"></el-table-column>
                    <el-table-column prop="remark" label="描述" align="center"></el-table-column>
                    <el-table-column prop="create_time" :formatter="dateFormat" label="创建时间" align="center"></el-table-column>
<!--                    <el-table-column label="操作"  align="center">-->
<!--                        <template slot-scope="scope">-->
<!--                            <el-button-->
<!--                                    type="text"-->
<!--                                    icon="el-icon-edit"-->
<!--                                    @click="handleEdit(scope.row)"-->
<!--                            >编辑-->
<!--                            </el-button>-->
<!--                            <el-button-->
<!--                                    type="text"-->
<!--                                    icon="el-icon-delete"-->
<!--                                    class="danger"-->
<!--                                    @click="handleDelete(scope.row)"-->
<!--                            >删除-->
<!--                            </el-button>-->
<!--                        </template>-->
<!--                    </el-table-column>-->
                </el-table>
                <div class="pagination">
                    <el-pagination
                            background
                            layout="total, prev, pager, next"
                            :current-page="query.pageIndex"
                            :page-size="query.pageSize"
                            :total="pageTotal"
                            @current-change="handlePageChange"
                    ></el-pagination>
                </div>
            </div>

            <!-- 编辑弹出框 -->
            <el-dialog title="编辑" :visible.sync="editVisible" width="30%">
                <el-form ref="form" :model="edit_form" label-width="100px">
                    <el-form-item label="告警策略名称">
                        <el-input v-model="edit_form.strategy_name"></el-input>
                    </el-form-item>
                    <el-form-item label="告警策略等级">
                        <el-input v-model="edit_form.strategy_level"></el-input>
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input type="textarea" v-model="edit_form.remark"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetedit" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
            </el-dialog>

            <!-- 新增弹出框 -->
            <el-dialog title="创建" :visible.sync="createVisible" width="30%">
                <el-form ref="form" :model="form" label-width="100px">
                    <el-form-item label="告警策略名称">
                        <el-input v-model="form.grade_name"></el-input>
                    </el-form-item>
                    <el-form-item label="告警策略等级">
                        <el-input v-model="form.grade_name"></el-input>
                    </el-form-item>
                    <el-form-item label="描述">
                        <el-input type="textarea" v-model="form.remark"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetCreate" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'alarmseverity',
        data() {
            return {
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                editVisible: false,
                createVisible: false,
                pageTotal: 0,
                edit_form:{},
                form: {},
                idx: -1,
                id: -1,
                searchData: {
                    strategy_name: '',
                    is_delete: 0
                },
                queryroomData: [{}],
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`monitor/api/alarm_strategy/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&strategy_name=${this.searchData.strategy_name}&is_delete=${this.searchData.is_delete}`, {
                    headers: {
                        'token':localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 创建操作
            handleCreate() {
                this.createVisible = true;
            },
            // 保存创建
            saveCreate() {
                this.$http.post(`monitor/api/alarm_strategy/`,
                    { 'strategy_name': this.form.strategy_name, 'strategy_level': this.form.strategy_level, 'remark': this.form.remark
                    },
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    if (res.status === 201) {
                        this.$message.success('创建成功！');
                        this.createVisible = false;
                        this.form = {};
                        this.getData()
                    } else {
                        this.$message.error('创建失败！');
                        this.form = {}
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 重置编辑
            resetedit() {
                this.getData();
                this.editVisible = false
            },

            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.form = {}
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning',
                    customClass: 'message-logout',
                    cancelButtonClass:'change_el_button'
                }).then(() => {this.$http.put(`monitor/api/alarm_strategy/${row.id}/logic_delete/`,
                    {'is_delete': 1},
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    if (res.status === 200) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    } else {
                        this.$message.error('删除失败！');
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    }

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            delAllSelection() {
                const length = this.multipleSelection.length;
                let str = '';
                this.delList = this.delList.concat(this.multipleSelection);
                for (let i = 0; i < length; i++) {
                    str += this.multipleSelection[i].name + ' ';
                }
                this.$message.error(`删除了${str}`);
                this.multipleSelection = [];
            },
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.edit_form = row;
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                this.$http.put(`monitor/api/alarm_strategy/${this.id}/`,
                    { 'strategy_name': this.edit_form.strategy_name, 'strategy_level': this.edit_form.strategy_level, 'remark': this.edit_form.remark },
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    console.log('Response:' + JSON.stringify(res));
                    if (res.status === 200) {
                        this.$message.success('修改成功！');
                        this.editVisible = false;
                        this.getData()
                    } else {
                        this.$message.error('修改失败！');
                        this.getData()
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            //处理时间格式
            dateFormat(row, column){
                const daterc = row[column.property]
                if(daterc!=null){
                    const dateMat = new Date(daterc);
                    const year = dateMat.getFullYear();
                    const month = dateMat.getMonth() + 1;
                    const day = dateMat.getDate();
                    const hh = dateMat.getHours();
                    const mm = dateMat.getMinutes();
                    const ss = dateMat.getSeconds();
                    const timeFormat = year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
                    return timeFormat;
                }
            },
        }
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve";
    @import "../../../assets/scss/darkStyle";
    .handle-box {
        margin-bottom: 20px;
    }

    .handle-select {
        width: 120px;
    }

    .handle-input {
        width: 300px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
    }

    .red {
        color: #ff0000;
    }

    .mr10 {
        margin-right: 10px;
    }

    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>
<style>
    .message-logout{
        background-color:#24273e;
        border: 1px solid #3c4163;
        color:#fff;
    }
    .el-message-box__title{
        color:#409EFF;
    }
    .el-message-box__content{
        color:#fff;
    }
    .change_el_button{
        background: #2a2e49;
        border: 1px solid #2f3561;
        color:#fff;
    }
</style>
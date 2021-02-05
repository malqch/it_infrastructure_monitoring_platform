<template>
    <div>
        <div class="wrapper">
            <!--<div class="crumbs">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>
                        <i class="el-icon-lx-cascades"></i> 服务器监控项
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div>-->
            <div class="container">
                <el-form :inline="true" v-model="form">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <div>
                            <el-button
                                    type="primary"
                                    icon="el-icon-circle-plus-outline"
                                    @click="handleCreate()"
                                    class="handle-box-1"
                            >增加
                            </el-button>
                        </div>
                        <div type="flex" class="row-bg" justify="end">
                            <el-form :inline="true" >
                                <el-form-item>
                                    <el-input v-model="searchData.monitor_type" clearable placeholder="监控类型" class="handle-input"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-input v-model="searchData.specific_type" clearable placeholder="具体监控对象" class="handle-input"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-input v-model="searchData.indicator" clearable placeholder="指标项" class="handle-input"></el-input>
                                </el-form-item>
                                <el-form-item>
                                    <el-input v-model="searchData.indicator_name" clearable placeholder="指标项名称" class="handle-input"></el-input>
                                </el-form-item>
                                <el-button icon="el-icon-search" type="primary" class="handle-box change_el_button" @click="handleSearch">查询</el-button>
                            </el-form>
                        </div>
                    </el-row>
                </el-form>
                <el-table
                        :data="tableData"
                        border
                        ref="multipleTable"
                        header-cell-class-name="table-header"
                        @selection-change="handleSelectionChange"
                >
                    <el-table-column type="selection"  align="center"></el-table-column>
                    <el-table-column prop="id" label="序号" align="center"></el-table-column>
                    <el-table-column prop="monitor_type" label="监控类型" align="center"></el-table-column>
                    <el-table-column prop="specific_type" label="具体监控对象" align="center"></el-table-column>
                    <el-table-column prop="indicator" label="指标项" align="center"></el-table-column>
                    <el-table-column prop="indicator_name" label="指标项名称" align="center"></el-table-column>
                    <el-table-column prop="remark" label="备注" align="center"></el-table-column>
                    <el-table-column prop="is_available" label="告警可用" align="center"></el-table-column>
                    <el-table-column prop="create_time" :formatter="dateFormat" label="创建时间" align="center"></el-table-column>
                    <el-table-column label="操作"  align="center">
                        <template slot-scope="scope">
                            <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    @click="handleEdit(scope.row)"
                            >编辑
                            </el-button>
                            <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="danger"
                                    @click="handleDelete(scope.row)"
                            >删除
                            </el-button>
                        </template>
                    </el-table-column>
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
                    <el-form-item label="监控类型">
                        <el-select style="width:100%" v-model="edit_form.monitor_type" @change="cleartype">
                            <el-option v-for="item in type_options"
                                       :key=item.value
                                       :label=item.label
                                       :value=item.value>
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-if="edit_form.monitor_type==='server'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="edit_form.specific_type">
                            <el-option value="Linux/Windows"></el-option>
                            <el-option value="Linux"></el-option>
                            <el-option value="Windows"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-else-if="edit_form.monitor_type==='data_base'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="edit_form.specific_type">
                            <el-option value="redis"></el-option>
                            <el-option value="dm"></el-option>
                            <el-option value="oracle"></el-option>
                            <el-option value="mysql"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-else-if="edit_form.monitor_type==='middleware'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="edit_form.specific_type">
                            <el-option value="webLogic"></el-option>
                            <el-option value="tomcat"></el-option>
                            <el-option value="rabbitMQ"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="指标项">
                        <el-input v-model="edit_form.indicator"></el-input>
                    </el-form-item>
                    <el-form-item label="指标项名称">
                        <el-input v-model="edit_form.indicator_name"></el-input>
                    </el-form-item>
                    <el-form-item label="告警可用">
                        <el-select style="width: 100%" v-model="edit_form.is_available">
                            <el-option value="可用"></el-option>
                            <el-option value="不可用"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="备注">
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
                    <el-form-item label="监控类型">
                        <el-select style="width:100%" v-model="form.monitor_type" @change="cleartype">
                            <el-option v-for="item in type_options"
                                       :key=item.value
                                       :label=item.label
                                       :value=item.value>
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-if="form.monitor_type==='server'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="form.specific_type">
                            <el-option value="Linux/Windows"></el-option>
                            <el-option value="Linux"></el-option>
                            <el-option value="Windows"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-else-if="form.monitor_type==='data_base'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="form.specific_type">
                            <el-option value="redis"></el-option>
                            <el-option value="dm"></el-option>
                            <el-option value="oracle"></el-option>
                            <el-option value="mysql"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item v-else-if="form.monitor_type==='middleware'" label="具体监控对象">
                        <el-select style="width: 100%" v-model="form.specific_type">
                            <el-option value="webLogic"></el-option>
                            <el-option value="tomcat"></el-option>
                            <el-option value="rabbitMQ"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="指标项">
                        <el-input v-model="form.indicator"></el-input>
                    </el-form-item>
                    <el-form-item label="指标项名称">
                        <el-input v-model="form.indicator_name"></el-input>
                    </el-form-item>
                    <el-form-item label="告警可用">
                        <el-select style="width: 100%" v-model="form.is_available">
                            <el-option value="可用"></el-option>
                            <el-option value="不可用"></el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="备注">
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
    import ElForm from "../../../../node_modules/element-ui/packages/form/src/form";
    export default {
        components: {ElForm},
        name: 'servermonitor',
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
                    monitor_type: '',
                    specific_type: '',
                    indicator: '',
                    indicator_name:'',
                    is_delete: 0
                },
                queryroomData: [{}],
                type_options: [
                    {"value":"server",
                    "label": "服务器"},
                    {"value":"middleware",
                    "label":"中间件"},
                    {"value":"data_base",
                    "label":"数据库"}
                ],
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`monitor/api/server_monitor/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&monitor_type=${this.searchData.monitor_type}&specific_type=${
                    this.searchData.specific_type}&indicator=${this.searchData.indicator}&indicator_name=${
                    this.searchData.indicator_name}&is_delete=${this.searchData.is_delete}`, {
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
                this.$http.post(`monitor/api/server_monitor/`,
                    { 'monitor_type': this.form.monitor_type, 'specific_type': this.form.specific_type,
                        'indicator': this.form.indicator, 'indicator_name': this.form.indicator_name,
                        'remark': this.form.remark, 'is_available': this.form.is_available
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
                        this.searchData = {
                            monitor_type: '',
                            specific_type: '',
                            indicator: '',
                            indicator_name:'',
                            is_delete: 0
                        };
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
                this.editVisible = false;
                this.searchData = {
                    monitor_type: '',
                    specific_type: '',
                    indicator: '',
                    indicator_name:'',
                    is_delete: 0
                };
                this.getData();
            },

            //重置新增
            resetCreate(){
                this.createVisible = false;
                this.form = {};
                this.searchData = {
                    monitor_type: '',
                    specific_type: '',
                    indicator: '',
                    indicator_name:'',
                    is_delete: 0
                };
                this.getData()
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning',
                    customClass: 'message-logout',
                    cancelButtonClass:'change_el_button'
                }).then(() => {this.$http.put(`monitor/api/server_monitor/${row.id}/logic_delete/`,
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
                this.$http.put(`monitor/api/server_monitor/${this.id}/`,
                    { 'os_name': this.edit_form.os_name, 'index': this.edit_form.index,
                        'index_name': this.edit_form.index_name, 'remark': this.edit_form.remark, 'is_available':
                        this.edit_form.is_available },
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

            //
            cleartype() {
              this.edit_form.specific_type = ''
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
        width: 180px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
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

<template>
    <div>
        <div class="wrapper">
            <div class="container">
                <el-input
                        type="text"
                        placeholder="请输入中间件名称"
                        v-model="keywords"
                        clearable
                        style="width:200px; margin-bottom:15px;">
                </el-input>
                <el-button style="margin-left:10px;" @click="handleSearch" class="change_el_button">查询</el-button>
                <el-button
                        type="primary"
                        icon="el-icon-circle-plus-outline"
                        @click="handleCreate" >新增</el-button>
                <el-table
                        :data="tableData"
                        border
                        style="width: 100%"
                        max-height="600"
                        class="user-table"
                >
                    <el-table-column type="selection" align="center"></el-table-column>
                    <el-table-column type="index" label="序号" align="center"></el-table-column>
                    <el-table-column prop="name" label="中间件名称" align="center" width="120"></el-table-column>
                    <el-table-column prop="middleware_type" label="中间件类型" align="center" width="120"></el-table-column>
                    <el-table-column prop="ip_address" label="中间件IP" align="center"></el-table-column>
                    <el-table-column prop="port" label="端口号" align="center"></el-table-column>
                    <el-table-column prop="username" label="用户名" align="center"></el-table-column>
                    <el-table-column prop="main_mode" label="维护模式" align="center"></el-table-column>
                    <af-table-column prop="is_monitor" label="是否监控" align="center"></af-table-column>
                    <el-table-column label="操作" width="200" align="center">
                        <template slot-scope="scope">
                            <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    @click="handleEdit(scope.$index, scope.row)"
                            >编辑</el-button>
                            <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="danger"
                                    @click="handleDelete(scope.$index, scope.row)"
                            >删除</el-button>
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
            <el-dialog :title="title" :visible.sync="editVisible" width="30%">
                <el-form ref="form" :rules="rules" :model="form" label-width="93px">
                    <el-form-item label="中间件名称" prop="name">
                        <el-input v-model="form.name"></el-input>
                    </el-form-item>
                    <el-form-item label="中间件类型" prop="middleware_type">
                        <el-select v-model="form.middleware_type" placeholder="请选择" :popper-append-to-body="false">
                            <el-option
                                    v-for="item in options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="IP地址" prop="ip_address">
                        <el-input v-model="form.ip_address"></el-input>
                    </el-form-item>
                    <el-form-item label="端口号" prop="port">
                        <el-input v-model="form.port"></el-input>
                    </el-form-item>
                    <el-form-item label="用户名" prop="username">
                        <el-input v-model="form.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码" prop="password">
                        <el-input type="password" v-model="form.password"></el-input>
                    </el-form-item>
                    <el-form-item label="维护模式" prop="main_mode">
                        <el-select v-model="form.main_mode">
                            <el-option
                                    v-for="item in options_main_mode"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="是否监控" prop="is_monitor">
                        <el-select v-model="form.is_monitor">
                            <el-option v-for="item in is_monitor_options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="editVisible = false" class="change_el_button">取 消</el-button>
                    <el-button type="primary" @click="saveEdit">确 定</el-button>
                </span>
            </el-dialog>
            <!-- 删除中间件信息弹出框 -->
            <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
                <span>确定要删除 {{ name }} 中间件信息吗？</span>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="deleteVisible = false" class="change_el_button">取 消</el-button>
                    <el-button type="primary" @click="deleteDB">确 定</el-button>
                </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                options_main_mode: [{
                    value: '否',
                    label: '否'
                }, {
                    value: '是',
                    label: '是'
                }],
                is_monitor_options:[{
                    value: "是"
                },{
                    value: "否"
                }],
                options: [{
                    value: 'WEBLOGIC',
                    label: 'WEBLOGIC'
                }, {
                    value: 'REDIS',
                    label: 'REDIS'
                }, {
                    value: 'TOMCAT',
                    label: 'TOMCAT'
                }, {
                    value: 'RABBITMQ',
                    label: 'RABBITMQ'
                }, {
                    value: 'WEBSPHERE',
                    label: 'WEBSPHERE'
                    }],
                keywords: '',
                title: '',
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
                assignVisible: false,
                deleteVisible: false,
                pageTotal: 0,
                form:{},
                idx: -1,
                id: -1,
                rules: {
                    name: [
                        { required: true, message: '请输入中间件名称', trigger: 'blur' },
                    ],
                    ip_address: [
                        { required: true, message: '请输入中间件地址', trigger: 'blur' },
                    ]
                },
                name: ''
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword = this.keywords;
                let url = this.url;
                if (keyword) {
                    url = `monitor/api/middleware/?name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url = `monitor/api/middleware/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }
                this.$http.get(`${url}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch(  (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 触发删除按钮
            handleDelete(index, row) {
                this.id = row.id;
                this.form = row;
                this.name = row.name;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteDB() {
                this.$http.put(`monitor/api/middleware/delete/`,
                    {'ids': [this.id]},
                    {
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('删除成功！');
                        this.deleteVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('删除失败！');
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
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
            handleEdit(index, row) {
                this.id = row.id;
                this.form = row;
                this.title = '编辑';
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 新增操作
            handleCreate() {
                this.title = "新增";
                this.editVisible = true;
                this.createVisible = false;
                this.form = {};
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$refs.form.validate((valid) => {
                            if (valid) {
                                this.$http.put(`monitor/api/middleware/${this.id}/`,
                                    this.form,
                                    {
                                        headers:{
                                            'token': localStorage.getItem('token')
                                        }
                                    }).then((res)=>{
                                    if(res.status === 200) {
                                        this.$message.success('修改成功！');
                                        this.editVisible = false;
                                        this.getData();
                                    }else{
                                        this.$message.error('修改失败！');
                                    }
                                }).catch( (error) =>{
                                    this.$message.error(JSON.stringify(error.response.data));
                                });
                            } else {
                                this.$message.warning('参数错误');
                                return false;
                            }
                        });
                }else {
                    this.$refs.form.validate((valid) => {
                            if (valid) {
                                this.$http.post(`monitor/api/middleware/`,
                                    this.form,
                                    {
                                        headers:{
                                            'token': localStorage.getItem('token')
                                        }
                                    }).then((res)=>{
                                    if(res.status === 200 || res.status === 201) {
                                        this.$message.success('创建成功！');
                                        this.editVisible = false;
                                        this.getData();
                                    }else{
                                        this.$message.error('创建失败！');
                                    }
                                }).catch( (error) =>{
                                    this.$message.error(JSON.stringify(error.response.data));
                                });
                            } else {
                                this.$message.warning('参数错误');
                                return false;
                            }
                        });
                }
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            }
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

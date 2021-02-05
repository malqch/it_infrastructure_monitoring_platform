<template>
    <div>
        <div class="wrapper">
            <div class="crumbs">
                <el-breadcrumb separator="/">
                </el-breadcrumb>
            </div>
            <div class="container">
                <el-input
                        type="text"
                        placeholder="请输入数据库监控项名称"
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
                    <el-table-column prop="db_type" label="数据库类型" align="center" width="120"></el-table-column>
                    <el-table-column prop="item" label="监控项" align="center"></el-table-column>
                    <el-table-column prop="item_name" label="监控项名称" align="center"></el-table-column>
                    <el-table-column prop="is_available" label="告警可用" align="center"></el-table-column>
                    <el-table-column prop="remark" label="备注" align="center"></el-table-column>
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
                    <el-form-item label="数据库类型" prop="db_type">
                        <el-select v-model="form.db_type" placeholder="请选择" :popper-append-to-body="false">
                            <el-option
                                    v-for="item in options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="监控项名称" prop="item_name">
                        <el-input v-model="form.item_name"></el-input>
                    </el-form-item>
                    <el-form-item label="监控项" prop="item">
                        <el-input v-model="form.item"></el-input>
                    </el-form-item>
                    <el-form-item label="告警可用" prop="is_available">
                        <el-select v-model="form.is_available" placeholder="请选择" :popper-append-to-body="false">
                            <el-option
                                    v-for="item in is_available_options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="备注" prop="remark">
                        <el-input v-model="form.remark"></el-input>
                    </el-form-item>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
            </el-dialog>
            <!-- 删除数据库信息弹出框 -->
            <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
                <span>确定要删除 {{ db_type}} - {{item }} 数据库监控项信息吗？</span>
                <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="deleteDBItem">确 定</el-button>
            </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                is_available_options:[{
                    value: '不可用',
                    label: '不可用'
                },{
                    value: '可用',
                    label: '可用'
                }],
                options: [{
                    value: 'MYSQL',
                    label: 'MYSQL'
                }, {
                    value: 'ORACLE',
                    label: 'ORACLE'
                }, {
                    value: 'DAMENG',
                    label: '达梦'
                }, {
                    value: 'POSTGRESQL',
                    label: 'POSTGRESQL'
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
                    item_name: [
                        { required: true, message: '请输入监控项中文名称', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 个字符', trigger: 'blur' }
                    ],
                    item: [
                        { required: true, message: '请输入监控项', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 位之间', trigger: 'blur' }
                    ],
                    db_type: [
                        { required: true, message: '请输入数据库类型', trigger: 'blur' },
                    ]
                },
                db_type: '',
                item: ''
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
                    url=`monitor/api/dbitem/?item_name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url=`monitor/api/dbitem/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
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
                this.db_type = row.db_type;
                this.item = row.item;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteDBItem() {
                this.$http.delete(`monitor/api/dbitem/${this.id}/`,
                    {
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res)=>{
                    if(res.status === 204) {
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
            },
            // 新增操作
            handleCreate() {
                this.title = "新增";
                this.editVisible = true;
                this.createVisible = false;
                this.form = {};
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$http.put(`monitor/api/dbitem/${this.id}/`,
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
                }else {
                    this.$http.post(`monitor/api/dbitem/`,
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

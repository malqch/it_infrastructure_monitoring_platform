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
                        placeholder="请输入存储信息名"
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
                    <el-table-column prop="storage_type" label="存储类型" align="center" width="120"></el-table-column>
                    <el-table-column prop="item_name" label="监控项名称" align="center"></el-table-column>
                    <el-table-column prop="item_obj" label="监控对象" align="center">
                        <template scope="scope" style="font-size: 10px">
                            <span v-if="scope.row.item_obj=='11'">{{"LUN"}}</span>
                            <span v-else-if="scope.row.item_obj=='207'">{{"控制器"}}</span>
                            <span v-else-if="scope.row.item_obj=='216'">{{"存储池"}}</span>
                            <span v-else-if="scope.row.item_obj=='213'">{{"以太网口"}}</span>
                        </template>
                    </el-table-column>
                    <el-table-column prop="item" label="监控项" align="center"></el-table-column>
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
                    <el-form-item label="存储类型" prop="storage_type">
                        <el-select v-model="form.storage_type" placeholder="请选择" :popper-append-to-body="false">
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
                    <el-form-item label="监控对象" prop="item_obj">
                        <el-select v-model="form.item_obj" placeholder="请选择" :popper-append-to-body="false">
                            <el-option
                                    v-for="item in item_obj_options"
                                    :key="item.value"
                                    :label="item.label"
                                    :value="item.value">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="监控项" prop="item">
                        <el-input v-model="form.item"></el-input>
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
            <!-- 删除存储信息弹出框 -->
            <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
                <span>确定要删除 {{ storage_type}} - {{item }} 存储监控项信息吗？</span>
                <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false" class="change_el_button">取 消</el-button>
                <el-button type="primary" @click="deletestorageitem">确 定</el-button>
            </span>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                options: [{
                    value: 'HUAWEI',
                    label: 'HUAWEI'
                }],
                item_obj_options: [{
                    value: '11',
                    label: 'LUN'
                },{
                    value: '207',
                    label: '控制器'
                },{
                    value: '216',
                    label: '存储池'
                },{
                    value: '213',
                    label: '以太网口'
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
                    item_obj: [
                        { required: true, message: '请输入监控对象', trigger: 'blur' },
                        { min: 1, max: 50, message: '长度在 1 到 50 位之间', trigger: 'blur' }
                    ],
                    storage_type: [
                        { required: true, message: '请输入存储类型', trigger: 'blur' },
                    ]
                },
                storage_type: '',
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
                    url=`monitor/api/storageitem/?item_name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url=`monitor/api/storageitem/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
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
                this.storage_type = row.storage_type;
                this.item = row.item;
                this.deleteVisible = true;
            },
            // 删除操作
            deletestorageitem() {
                this.$http.delete(`monitor/api/storageitem/${this.id}/`,
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
                this.form = {};
                this.title = "新增";
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$http.put(`monitor/api/storageitem/${this.id}/`,
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
                    this.$http.post(`monitor/api/storageitem/`,
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

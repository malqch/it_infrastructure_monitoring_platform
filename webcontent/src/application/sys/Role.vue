<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row type="flex" class="row-bg" justify="space-between">
                <div>
                    <el-button
                            type="primary"
                            icon="el-icon-circle-plus-outline"
                            @click="handleCreate" v-if="hasPerm('sys:role:add')">新增</el-button>
                </div>
                <div>
                    <el-input
                            type="text"
                            placeholder="请输入角色名"
                            v-model="keywords"
                            style="width:200px; margin-bottom:15px;"
                            clearable>
                    </el-input>
                    <el-button style="margin-left:10px;" type="primary" @click="handleSearch" v-if="hasPerm('sys:role:list')">查询</el-button>
                </div>
            </el-row>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="name" label="名字" align="center"></el-table-column>
                <el-table-column prop="mark" label="权限" align="center"></el-table-column>
                <el-table-column prop="create_time" label="创建时间" :formatter="datetimeFormat" align="center"></el-table-column>
                <el-table-column label="操作" width="250" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-s-operation"
                                class="color-link"
                                @click="handleMenu(scope.$index, scope.row)"
                                v-if="hasPerm('sys:role:assign_menu')"
                        >分配菜单</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
                                v-if="hasPerm('sys:role:modify')"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                                v-if="hasPerm('sys:role:delete')"
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
            <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                <el-form-item label="角色名称" prop="name">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="权限" prop="mark">
                    <el-input v-model="form.mark"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 菜单分配弹出框 -->
        <el-dialog title="分配菜单" :visible.sync="menuVisible" width="60%">
            <tree-transfer :title="tree_title" :from_data='fromDataTree' :to_data='toDataTree' :defaultProps="{label:'name'}" @addBtn='add' @removeBtn='remove' height='340px' filter openAll>
            </tree-transfer>
        </el-dialog>
        <!-- 删除角色弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除 {{name}} 角色吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteRole">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { treeDataTranslate } from '../../util/formatData'
    import { datetimeFormat } from '../../util/formatData'
    import treeTransfer from 'el-tree-transfer'
    export default {
        name: 'roletable',
        mode: "transfer", // transfer addressList
        data() {
            return {
                options: [],
                menu_radios: [],
                menu_options: [],
                button_options: [],
                menuProps: {
                    value: 'id',
                    label: 'name',
                    multiple: true
                },
                keywords: '',
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                title: '',
                name:'',
                editVisible: false,
                menuVisible: false,
                deleteVisible: false,
                pageTotal: 0,
                datetimeFormat: null,
                loading: true,
                form: {},
                idx: -1,
                id: -1,
                tree_title:['未分配','已分配'],
                fromDataTree:[],
                toDataTree:[],
                rules: {
                    name: [
                        { required: true, message: '请输入角色名', trigger: 'blur' },
                        { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }
                    ],
                    mark: [
                        { required: true, message: '请输入权限', trigger: 'blur' },
                    ]
                },
            };

        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getData();
            this.datetimeFormat = datetimeFormat;
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword=this.keywords;
                let url=this.url;
                if(keyword) {
                    url=`sys/api/role/?name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url=`sys/api/role/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }
                this.$http.get(url, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                    this.loading = false;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
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
            deleteRole() {
                this.$http.put(`sys/api/role/delete/`,
                    {'ids': [this.id]},
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('删除成功！');
                        this.deleteVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('删除失败！');
                    }
                }).catch(  (error) =>{
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
                this.title = "编辑";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 新增操作
            handleCreate() {
                this.form = {};
                this.title = "新增";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                if(this.title==="编辑") {
                    this.$refs.form.validate((valid) => {
                        if (valid) {
                            this.$http.put(`sys/api/role/${this.id}/`,
                                this.form,
                                {
                                    headers:{
                                        'token': this.token
                                    }
                                }).then((res)=>{
                                if(res.status === 200) {
                                    this.$message.success('修改成功！');
                                    this.editVisible = false;
                                    this.getData();
                                }else{
                                    this.$message.success('修改失败！');
                                }
                            }).catch( (error) => {
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
                            this.$http.post(`sys/api/role/`,
                                this.form,
                                {
                                    headers:{
                                        'token': this.token
                                    }
                                }).then((res)=>{
                                if(res.status === 200 || res.status === 201) {
                                    this.$message.success('创建成功！');
                                    this.editVisible = false;
                                    this.getData();
                                }else{
                                    this.$message.success('创建失败！');
                                }
                            }).catch( (error) => {
                                this.$message.error(JSON.stringify(error.response.data));
                            });
                            } else {
                                this.$message.warning('参数错误');
                                return false;
                            }
                    });
                }

            },
            // 查询未分配菜单栏数据
            getMenus() {
                this.$http.get(`sys/api/role/${this.id}/to_menu/`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    console.log(res.data, 8983998888)
                    this.fromDataTree = treeDataTranslate(res.data, 'id');
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 查询已分配菜单栏数据
            getToMenus() {
                this.$http.get(`sys/api/role/${this.id}/menu/`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.toDataTree = treeDataTranslate(res.data, 'id');
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 分配菜单栏操作
            handleMenu(index, row) {
                this.id = row.id;
                this.name = row.name;
                this.getMenus();
                this.getToMenus();
                this.menuVisible = true;
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            // 监听穿梭框组件添加
            add(fromDataTree,toDataTree,obj){
                // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的{keys,nodes,halfKeys,halfNodes}对象
                let obj_nodes=obj.nodes;
                let get_obj=[];
                obj_nodes.map( item =>{ get_obj.push(item.id) });
                this.$http.put(`sys/api/role/${this.id}/assign_menu/`,
                    {"menus": get_obj},
                    {
                        headers:{
                            'token': this.token
                        }
                }).then(()=>{
                    fromDataTree = this.getMenus();
                    toDataTree = this.getToMenus();
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 监听穿梭框组件移除
            remove(fromDataTree,toDataTree,obj){
                // 树形穿梭框模式transfer时，返回参数为左侧树移动后数据、右侧树移动后数据、移动的{keys,nodes,halfKeys,halfNodes}对象
                let obj_nodes=obj.nodes;
                let get_obj=[];
                obj_nodes.map( item =>{
                    get_obj.push(item.id);
                });
                this.$http.put(`sys/api/role/${this.id}/remove_menu/`,
                    {"menus": get_obj},
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then(()=>{
                        fromDataTree = this.getMenus();
                        toDataTree = this.getToMenus();
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            }
        },
        components:{ treeTransfer }, // 注册
    };
</script>

<style lang="scss" scoped>
    @import "../../assets/scss/serve.scss";
    .tag_margin{
        margin:5px 5px 0 0;
    }
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

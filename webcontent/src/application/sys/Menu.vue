<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-button
                    type="primary"
                    icon="el-icon-circle-plus-outline"
                    style="margin-bottom:15px;"
                    @click="handleCreate" v-if="hasPerm('sys:menu:add')">新增</el-button>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    row-key="id"
                    style="width: 100%">
                <el-table-column prop="name" label="名称" header-align="center"></el-table-column>
                <el-table-column prop="prev_menu" label="上级菜单" align="center"></el-table-column>
                <el-table-column prop="icon" label="图标" align="center">
                    <template slot-scope="scope">
                        <i :class="scope.row.icon"></i>
                    </template>
                </el-table-column>
                <el-table-column prop="menu_type" label="类型" align="center">
                    <template slot-scope="scope">
                        <el-tag v-if="scope.row.menu_type === 'dir'" size="small">目录</el-tag>
                        <el-tag v-else-if="scope.row.menu_type === 'menu'" size="small" type="success">菜单</el-tag>
                        <el-tag v-else-if="scope.row.menu_type === 'button'" size="small" type="info">按钮</el-tag>
                    </template>
                </el-table-column>
                <el-table-column prop="perms" label="授权标识" align="center"></el-table-column>
<!--                <el-table-column prop="menu_url" label="菜单URL" align="center"></el-table-column>-->
                <el-table-column label="操作" width="180" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
                                v-if="hasPerm('sys:menu:modify')"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                                v-if="hasPerm('sys:menu:delete')"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 编辑弹出框 -->
        <el-dialog :title="title" :visible.sync="editVisible" width="30%">
            <el-form :model="form" :rules="rules" ref="form" label-width="100px">
                <el-form-item label="类型" prop="menu_type">
                    <el-radio-group v-model="form.menu_type">
                        <el-radio v-for="item in typeList"
                                  :label="item.e_name"
                                  :key="item.id"
                                  :value="item.e_name">{{ item.c_name }}</el-radio>
                    </el-radio-group>
                </el-form-item>
                <el-form-item :label="'名称'" prop="name">
                    <el-input v-model="form.name" :placeholder="'名称'"></el-input>
                </el-form-item>
                <el-form-item v-if="form.menu_type !== 'dir'" label="上级菜单" prop="prev_menu">
                    <el-input v-model="form.prev_menu"
                              placeholder="点击选择上级菜单"
                              @click.native="changeSelectTree"></el-input>
                    <el-tree
                            v-show="isShowSelect"
                            empty-text="暂无数据"
                            :data="menuList"
                            :props="menuListTreeProps"
                            node-key="id"
                            ref="selectTree"
                            @node-click="selectClassfy"
                            :default-expand-all="false"
                            :highlight-current="true"
                            :expand-on-click-node="true">
                    </el-tree>
                </el-form-item>
<!--                <el-form-item v-if="form.menu_type !== 'dir'" label="上级菜单" prop="prev_menu">-->
<!--                    <el-input v-model="form.prev_menu" placeholder="上级菜单"></el-input>-->
<!--                </el-form-item>-->
                <el-form-item v-if="form.menu_type === 'menu'" label="菜单URL" prop="menu_url">
                    <el-input v-model="form.menu_url" placeholder="菜单URL"></el-input>
                </el-form-item>
                <el-form-item v-if="form.menu_type === 'button'" label="授权标识" prop="perms">
                    <el-input v-model="form.perms" placeholder="授权标识,如:sys:user:list"></el-input>
                </el-form-item>
                <el-form-item v-if="form.menu_type === 'dir'" label="英文标识" prop="application">
                    <el-input v-model="form.application" placeholder="英文标识"></el-input>
                </el-form-item>
                <el-form-item v-if="form.menu_type !== 'dir'" label="所属app" prop="application">
                    <el-select v-model="form.application" placeholder="请选择所属app">
                        <el-option
                                v-for="item in menu_options"
                                :key="item"
                                :label="item"
                                :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除用户弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除菜单 {{name}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteMenu">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { treeDataTranslate } from '../../util/formatData'
    export default {
        name: 'datacentertable',
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
                form: {},
                menu_options: [],
                typeList: [
                    // {   id: 0,
                    //     c_name: '目录',
                    //     e_name: 'dir'},
                    // {   id: 1,
                    //     c_name: '菜单',
                    //     e_name: 'menu'},
                    // {   id: 2,
                    //     c_name: '按钮',
                    //     e_name: 'button'}
                ],
                menuList: [],
                menuListTreeProps: {
                    label: 'name',
                    children: 'children'
                },
                title: '',
                editVisible: false,
                deleteVisible: false,
                isShowSelect: false,
                loading: true,
                rules: {
                    name: [
                        { required: true, message: '请输入菜单名', trigger: 'blur' },
                        { min: 2, max: 100, message: '长度在 2 到 100 个字符' }
                    ],
                    application: [
                        { required: true, message: '请输入app', trigger: 'input' }
                    ],
                    prev_menu: [
                        { required: true, message: '请选择上级菜单', trigger: 'input' }
                    ]
                },
                pageTotal: 0,
                idx: -1,
                id: -1,
                name:''
            };
        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`sys/api/menu/`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.tableData = treeDataTranslate(res.data, 'id');
                    this.loading = false;
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
                });
            },
            // 查询所有的app
            getApp() {
                this.$http.get(`sys/api/menu/app_list/`,
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                        this.menu_options = res.data;
                    }).catch( (error) => {
                        console.log("Error"+error);
                    this.$message.error(JSON.stringify(error.response.data));
                        // alert(error);
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
            deleteMenu() {
                this.$http.put(`sys/api/menu/delete/`,
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
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    // alert(error);
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
                if(row.menu_type==='dir') {
                    this.typeList = [
                        {   id: 0,
                            c_name: '目录',
                            e_name: 'dir'
                        }
                    ]
                }else if(row.menu_type==='menu') {
                    this.typeList = [
                        {   id: 1,
                            c_name: '菜单',
                            e_name: 'menu'
                        }
                    ]
                }else {
                    this.typeList = [
                        {   id: 2,
                            c_name: '按钮',
                            e_name: 'button'
                        }
                    ]
                }
                this.title = '编辑';
                this.menuList = this.tableData;
                this.getApp();
                this.editVisible = true;
                console.log(this.form.menu_type);
                console.log(this.typeList);
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$http.put(`sys/api/menu/${this.id}/`,
                        this.form,
                        {
                            headers:{
                                'token': this.token
                            }
                        }).then((res)=>{
                        if(res.status === 200) {
                            this.$message.success('修改成功！');
                            this.editVisible = false;
                        }else{
                            this.$message.success('修改失败！');
                        }
                    }).catch(  (error) =>{
                        this.$message.error(JSON.stringify(error.response.data));
                        // alert("联网失败，请检查网络");
                    });
                }else {
                    this.$refs.form.validate((valid) => {
                        if (valid) {
                            this.$http.post(`sys/api/menu/`,
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
                            }).catch( (error) =>{
                                this.$message.error(JSON.stringify(error.response.data));
                                // alert(error);
                            });
                        } else {
                            this.$message.warning('请选择必填项');
                            return false;
                        }
                    });
                }
            },
            // 新增操作
            handleCreate() {
                this.typeList = [
                    {   id: 0,
                        c_name: '目录',
                        e_name: 'dir'},
                    {   id: 1,
                        c_name: '菜单',
                        e_name: 'menu'},
                    {   id: 2,
                        c_name: '按钮',
                        e_name: 'button'}];
                this.form = {
                    menu_type: 'menu',
                };
                this.title = "新增";
                this.menuList = this.tableData;
                this.getApp();
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 点击菜单树操作
            changeSelectTree() {
                this.isShowSelect=true;
            },
            // 选中菜单树操作
            selectClassfy(data) {
                this.form.prev_menu=data.name;
                this.isShowSelect=false;
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
    @import "../../assets/scss/serve.scss";
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

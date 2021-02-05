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
                        @click="handleCreate"
                        v-if="hasPerm('sys:user:add')">新增</el-button>
                </div>
                <div>
                    <el-input
                            type="text"
                            placeholder="请输入用户名"
                            v-model="keywords"
                            style="width:200px; margin-bottom:15px;" clearable>
                    </el-input>
                    <el-button style="margin-left:10px;" type="primary" @click="handleSearch" v-if="hasPerm('sys:user:list')">查询</el-button>
                </div>
            </el-row>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
                    class="user-table"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" align="center" width="120"></el-table-column>
                <el-table-column prop="email" label="邮箱" align="center" :show-overflow-tooltip=true></el-table-column>
                <el-table-column prop="phone" label="电话" align="center"></el-table-column>
                <el-table-column prop="create_time" label="创建时间" :formatter="datetimeFormat" align="center" :show-overflow-tooltip=true></el-table-column>
                <el-table-column prop="roles"  :formatter="roleFormat" label="角色" align="center" :show-overflow-tooltip=true></el-table-column>
                <el-table-column label="操作" width="300" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-s-custom"
                                class="color-link"
                                @click="handleRole(scope.$index, scope.row)"
                                v-if="hasPerm('sys:user:assign_role')"
                        >分配角色</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
                                v-if="hasPerm('sys:user:modify')"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-refresh"
                                class="color-link"
                                @click="handleReset(scope.$index, scope.row)"
                                v-if="hasPerm('sys:user:reset_pwd')"
                        >重置密码</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                                v-if="hasPerm('sys:user:delete')"
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
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="form.username"></el-input>
                </el-form-item>
                <el-form-item v-if="this.title==='新增'" label="密码" prop="password">
                    <el-input :type="this.registration_data.pwdType" v-model="form.password"></el-input>
                    <img v-if="this.form.password" :src="this.registration_data.src" @click="changeType" class="eye"/>
                </el-form-item>
                <el-form-item v-if="this.title==='新增'" label="确认密码" prop="confirm_pwd">
                    <el-input :type="this.registration_data.pwdConfirmType" v-model="form.confirm_pwd"></el-input>
                    <img v-if="this.form.confirm_pwd" :src="this.registration_data.srcConfirm" @click="changeConfirmType" class="eye"/>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="form.email"></el-input>
                </el-form-item>
                <el-form-item label="电话" prop="phone">
                    <el-input v-model="form.phone"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 角色分配弹出框 -->
        <el-dialog title="分配角色" :visible.sync="assignVisible" width="30%">
            <el-form ref="form" :model="assign_form" label-width="70px">
                                <el-form-item label="角色">
                                    <el-checkbox-group v-model="assign_form.roles">
                                        <el-checkbox
                                                v-for="item in check_roles"
                                                :key="item.id"
                                                :label="item.id">{{item.name}}
                                        </el-checkbox>
                                    </el-checkbox-group>
                                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="assignVisible = false">取 消</el-button>
                <el-button type="primary" @click="assignRole">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 密码重置弹出框 -->
        <el-dialog title="提示" :visible.sync="resetVisible" width="25%">
            <span>确定要重置密码吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resetVisible = false">取 消</el-button>
                <el-button type="primary" @click="resetPwd">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除用户弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除用户 {{username}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteUser">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { datetimeFormat } from '../../util/formatData'
    import { validatePhoneTwo, validateEMail } from '../../util/validate'

    export default {
        name: 'usertable',
        data() {
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入新密码'));
                } else if (value !== this.form.password) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                registration_data:{
                    pwdType: "password",
                    pwdConfirmType: "password",
                    src: require("../../assets/colse_eye.png"),
                    srcConfirm: require("../../assets/colse_eye.png")
                },
                check_roles: [],
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
                resetVisible: false,
                pageTotal: 0,
                form:{},
                assign_form: {
                    roles: [],
                },
                datetimeFormat: null,
                loading: true,
                idx: -1,
                id: -1,
                rules: {
                    username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 2, max: 10, message: '长度在 2 到 10 个字符', trigger: 'blur' }
                    ],
                    password: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 18, message: '长度在 6 到 18 位之间', trigger: 'blur' }
                    ],
                    confirm_pwd: [
                        { required: true, message: '请确认密码', trigger: 'blur' },
                        { validator: validatePass2, trigger: 'blur' }
                    ],
                    email: [
                        { required: true, message: '请输入邮箱', trigger: 'blur' },
                        { validator: validateEMail, trigger: 'blur'}
                    ],
                    phone: [
                        { required: true, message: '请输入电话', trigger: 'blur' },
                        { validator: validatePhoneTwo, trigger: 'blur'}
                    ]
                },
                username:''
            };
        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getData();
            this.datetimeFormat = datetimeFormat;
        },
        methods: {
            // 密码隐藏与显示
            changeType(){
                this.registration_data.pwdType = this.registration_data.pwdType==='password'?'text':'password';
                this.registration_data.src=this.registration_data.src==require("../../assets/colse_eye.png")?require("../../assets/open_eye.png"):require("../../assets/colse_eye.png");
            },
            changeConfirmType(){
                this.registration_data.pwdConfirmType = this.registration_data.pwdConfirmType==='password'?'text':'password';
                this.registration_data.srcConfirm=this.registration_data.srcConfirm==require("../../assets/colse_eye.png")?require("../../assets/open_eye.png"):require("../../assets/colse_eye.png");
            },
            // 获取用户的role信息
            roleFormat(row) {
                if (row.roles === []) {
                    return ''
                } else {
                    var role = '';
                    for (let v of row.roles){
                        role += ' ' + v.name;
                    }
                    return role;
                }
            },
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword = this.keywords;
                let url = this.url;
                if (keyword) {
                    url=`sys/api/user/?username=${keyword}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }else {
                    url=`sys/api/user/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`
                }
                    this.$http.get(`${url}`, {
                        headers: {
                            'token': this.token,
                        }
                    }).then((res) => {
                        this.tableData = res.data.data;
                        this.pageTotal = res.data.total_count;
                        this.loading = false;
                    }).catch(  (error) => {
                        console.log(error);
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
                this.username = row.username;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteUser() {
                this.$http.put(`sys/api/user/delete/`,
                    {'ids': [this.id]},
                    {
                        headers:{
                            'token': this.token,
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
            // 重置密码操作
            handleReset(index, row) {
                this.id = row.id;
                this.resetVisible = true;
            },
            // 重置密码
            resetPwd() {
                this.$http.get(`sys/api/user/${this.id}/reset_pwd/`,
                    {
                        headers:{
                            'token': this.token,
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('密码重置成功！');
                        this.resetVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('密码重置失败！');
                    }
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
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
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
                this.form = {role:[]};
                this.registration_data.pwdType = this.registration_data.pwdConfirmType = 'password';
                this.registration_data.src = this.registration_data.srcConfirm =  require("../../assets/colse_eye.png");
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$refs.form.validate((valid) => {
                        if (valid) {
                            this.$http.put(`sys/api/user/${this.id}/`,
                                this.form,
                                {
                                    headers:{
                                        'token': this.token,
                                    }
                                }).then((res)=>{
                                if(res.status === 200) {
                                    this.$message.success('修改成功！');
                                    this.editVisible = false;
                                    this.getData();
                                }else{
                                    this.$message.error('修改失败！');
                                }
                            }).catch(  (error) => {
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
                        this.$http.post(`sys/api/user/`,
                            this.form,
                            {
                                headers:{
                                    'token': this.token,
                                }
                            }).then((res)=>{
                            if(res.status === 200 || res.status === 201) {
                                this.$message.success('创建成功！');
                                this.editVisible = false;
                                this.getData();
                            }else{
                                this.$message.error('创建失败！');
                            }
                        }).catch(  (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                            } else {
                                this.$message.warning('参数错误');
                                return false;
                            }
                        });
                }
            },
            // 查询用户信息
            getCheckRoles() {
                this.$http.get(`sys/api/role/`, {
                    headers:{
                        'token': this.token,
                    }
                }).then((res)=>{
                    this.check_roles = res.data;
                }).catch(  (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 分配角色操作
            handleRole(index, row) {
                this.getCheckRoles();
                this.id = row.id;
                this.roles = this.roleFormat(row);
                let roles_arr=[];
                row.roles.map( item => { roles_arr.push(item.id)});
                this.assign_form.roles=roles_arr;
                this.assignVisible = true;
            },
            // 用户分配角色
            assignRole() {
                this.$http.put(`sys/api/user/${this.id}/assign_user/`,
                    this.assign_form,
                    {
                        headers:{
                            'token': this.token,
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('角色分配成功！');
                        this.assignVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('角色分配失败！');
                    }
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
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
    .eye{
        width: 21px;
        height: 15px;
        display: inline-block;
        cursor: pointer;
        position: absolute;
        right: 10px;
        top:8px
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

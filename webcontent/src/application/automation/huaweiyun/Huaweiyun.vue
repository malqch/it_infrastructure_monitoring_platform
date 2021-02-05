<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <div style="padding-bottom: 15px;">
                <el-button
                        type="primary"
                        icon="el-icon-circle-plus-outline"
                        @click="handleCreate">新增</el-button>
            </div>
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
                <el-table-column prop="hw_username" label="用户名" align="center" width="120"></el-table-column>
                <el-table-column prop="hw_password" label="密码" :formatter="format_pwd" align="center" width="120"></el-table-column>
                <el-table-column prop="hw_ip" label="ip" align="center"></el-table-column>
                <el-table-column prop="hw_address" label="地址" align="center"></el-table-column>
                <el-table-column prop="update_time" label="更新时间" :formatter="datetimeFormat" align="center"></el-table-column>
                <el-table-column prop="create_time" label="创建时间" :formatter="datetimeFormat" align="center"></el-table-column>
                <el-table-column label="操作" width="300" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                @click="handleEdit(scope.$index, scope.row)"
                        >编辑</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
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
            <el-form ref="form" :rules="rules" :model="form" label-width="70px">
                <el-form-item label="用户名" prop="hw_username">
                    <el-input v-model="form.hw_username"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="hw_password">
                    <el-input :type="this.registration_data.pwdType" v-model="form.hw_password"></el-input>
                    <img v-if="this.form.hw_password" :src="this.registration_data.src" @click="changeType" class="eye"/>
                </el-form-item>
                <el-form-item label="ip" prop="hw_ip">
                    <el-input v-model="form.hw_ip"></el-input>
                </el-form-item>
                <el-form-item label="地址" prop="hw_address">
                    <el-input v-model="form.hw_address"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除用户弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除环境 {{hw_address}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { datetimeFormat } from '../../../util/formatData'
    export default {
        name: 'usertable',
        data() {
            return {
                registration_data:{
                    pwdType: "password",
                    src: require("../../../assets/colse_eye.png"),
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
                deleteVisible: false,
                pageTotal: 0,
                form:{},
                datetimeFormat: null,
                loading: true,
                idx: -1,
                id: -1,
                rules: {
                    hw_username: [
                        { required: true, message: '请输入用户名', trigger: 'blur' },
                        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
                    ],
                    hw_password: [
                        { required: true, message: '请输入密码', trigger: 'blur' },
                        { min: 6, max: 99, message: '长度在 6 到 99 位之间', trigger: 'blur' }
                    ],
                    hw_ip: [
                        { required: true, message: '请输入ip', trigger: 'blur' },
                    ],
                    hw_address: [
                        { required: true, message: '请输入私有云地址', trigger: 'blur' },
                    ]
                },
                hw_address:''
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
                this.registration_data.src=this.registration_data.src==require("../../../assets/colse_eye.png")?require("../../../assets/open_eye.png"):require("../../../assets/colse_eye.png");
            },
            // 格式化密码展示
            format_pwd(row) {
                if(row.hw_password) {
                    return '******'
                }
            },
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`automation/api/huawei/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`, {
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
                this.hw_address = row.hw_address;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteEdit() {
                this.$http.delete(`automation/api/huawei/${this.id}/`,
                    {
                        headers:{
                            'token': this.token,
                        }
                    }).then((res)=>{
                    if(res.status === 200 || res.status === 204) {
                        this.$message.success('删除成功！');
                        this.deleteVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('删除失败！');
                        this.deleteVisible = false;
                    }
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.deleteVisible = false;
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
                this.registration_data.pwdType = this.registration_data.pwdConfirmType = 'password';
                this.registration_data.src = this.registration_data.srcConfirm =  require("../../../assets/colse_eye.png");
            },
            // 新增操作
            handleCreate() {
                this.form = {};
                this.title = "新增";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
                this.registration_data.pwdType = this.registration_data.pwdConfirmType = 'password';
                this.registration_data.src = this.registration_data.srcConfirm =  require("../../../assets/colse_eye.png");
            },
            // 保存编辑
            saveEdit() {
                if(this.title === '编辑') {
                    this.$http.put(`automation/api/huawei/${this.id}/`,
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
                            this.editVisible = false;
                        }
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                        this.editVisible = false;
                    });
                }else {
                    this.$refs.form.validate((valid) => {
                        if (valid) {
                            this.$http.post(`automation/api/huawei/`,
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
                                    this.editVisible = false;
                                }
                            }).catch(  (error) => {
                                this.$message.error(JSON.stringify(error.response.data));
                                this.editVisible = false;
                            });
                        } else {
                            this.$message.warning('请选择必填项');
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
    @import "../../../assets/scss/serve.scss";
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

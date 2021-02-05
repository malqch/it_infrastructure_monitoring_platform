<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row :gutter="20">
                <el-col :span="10" :offset="7">
                    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px">
                        <el-form-item label="原密码" prop="old_pwd">
                            <el-input
                                    type="password"
                                    placeholder="原密码"
                                    v-model="ruleForm.old_pwd"
                                    style="width:260px;" autocomplete="off">
                            </el-input>
                        </el-form-item>
                        <el-form-item label="新密码" prop="new_pwd">
                            <el-input
                                    type="password"
                                    placeholder="新密码"
                                    v-model="ruleForm.new_pwd"
                                    style="width:260px;" autocomplete="off">
                            </el-input>
                        </el-form-item>
                        <el-form-item label="确认密码" prop="confirm_pwd">
                            <el-input
                                    type="password"
                                    placeholder="确认密码"
                                    v-model="ruleForm.confirm_pwd"
                                    style="width:260px;" autocomplete="off">
                            </el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-button @click="resetForm('ruleForm')">重置</el-button>
                            <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
                        </el-form-item>
                    </el-form>
                </el-col>
            </el-row>

        </div>
    </div>
</template>

<script>
    export default {
        data() {
            var validateOldPass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入原密码'));
                } else {
                    callback();
                }
            };
            var validateNewPass = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请输入新密码'));
                } else {
                    if (this.ruleForm.confirm_pwd !== '') {
                        this.$refs.ruleForm.validateField('confirm_pwd');
                    }
                    callback();
                }
            };
            var validatePass2 = (rule, value, callback) => {
                if (value === '') {
                    callback(new Error('请再次输入新密码'));
                } else if (value !== this.ruleForm.new_pwd) {
                    callback(new Error('两次输入密码不一致!'));
                } else {
                    callback();
                }
            };
            return {
                tableData: [],
                multipleSelection: [],
                delList: [],
                username: '',
                ruleForm: {
                    old_pwd: '',
                    new_pwd: '',
                    confirm_pwd: '',
                },
                idx: -1,
                id: -1,
                rules: {
                    old_pwd: [
                        { validator: validateOldPass, trigger: 'blur' },
                        { min: 6, max: 18, message: '长度在 6 到 18 位之间', trigger: 'blur' }
                    ],
                    new_pwd: [
                        { validator: validateNewPass, trigger: 'blur' },
                        { min: 6, max: 18, message: '长度在 6 到 18 位之间', trigger: 'blur' }
                    ],
                    confirm_pwd: [
                        { validator: validatePass2, trigger: 'blur' },
                        { min: 6, max: 18, message: '长度在 6 到 18 位之间', trigger: 'blur' }
                    ]
                },
            };
        },
        methods: {
            submitForm(formName) {
                this.$refs[formName].validate((valid) => {
                    if (valid) {
                        let username = localStorage.getItem('username');
                        let token = localStorage.getItem('token');
                        this.$http.put(`sys/api/user/change_pwd/`,
                            {'username': username, 'old_pwd': this.ruleForm.old_pwd, 'new_pwd': this.ruleForm.new_pwd},
                            {
                                headers:{
                                    'token': token
                                }
                            }).then((res)=>{
                            if(res.status === 200) {
                                this.$message.success('密码修改成功！');
                                this.$router.push('/login');
                            }else{
                                this.$message.error('密码修改失败！');
                            }
                        }).catch(  (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                            // alert("联网失败，请检查网络");
                        });
                    } else {
                        this.$message.error('密码修改失败！');
                        // console.log('error submit!!');
                        return false;
                    }
                });
            },
            resetForm(formName) {
                this.$refs[formName].resetFields();
            }
        }
    };
</script>

<template>
    <div class="login-wrap">
        <div class="ms-login">
            <div class="ms-title">运维监控管理平台</div>
            <el-form :model="param" :rules="rules" ref="login" label-width="0px" class="ms-content">
                <el-form-item prop="username">
                    <el-input v-model="param.username" placeholder="请输入用户名">
                        <el-button slot="prepend"><img src="../../assets/img/loginuser.png" style="width: 15px;height: 15px;margin-top: 3px;"></el-button>
                    </el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input
                            type="password"
                            placeholder="请输入密码"
                            v-model="param.password"
                            @keyup.enter.native="submitForm()"
                    >
                        <el-button slot="prepend"><img src="../../assets/img/loginpw.png" style="width: 15px;height: 15px;margin-top: 3px;"></el-button>
                    </el-input>
                </el-form-item>
                <div class="login-btn">
                    <el-button type="primary" @click="submitForm()">登录</el-button>
                </div>
<!--                <p class="login-tips">Tips : 用户名和密码随便填。</p>-->
            </el-form>
        </div>
    </div>
</template>

<script>
    import Vue from "vue";

    export default {
        data: function() {
            return {
                param: {
                    username: '',
                    password: ''
                },
                rules: {
                    username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
                    password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
                }
            };
        },
        methods: {
            submitForm() {
                this.$http.post(`sys/api/auth/`, null, {
                    headers: {
                        'username': this.param.username,
                        'password': this.param.password
                    }
                }).then((res) => {
                    console.log('Response:' + JSON.stringify(res));
                    if (res.status === 200) {
                        this.$message.success(res.data.msg);
                        localStorage.setItem('token', res.data.token);
                        localStorage.setItem('username', this.param.username);
                        this.$router.push('/index');
                    } else {
                        this.$message.error(res.data.msg);
                    }
                }).catch(function(error) {
                    // console.log('Error' + JSON.stringify(error.response.data));
                    Vue.prototype.$message.warning(JSON.stringify(error.response.data));
                });
            }
        }
    };
</script>

<style scoped>
    .login-wrap {
        position: relative;
        width: 100%;
        height: 100%;
        background-image: url(../../assets/img/login-bg.jpg);
        background-size: 100%;
    }
    .ms-title {
        width: 100%;
        line-height: 50px;
        text-align: center;
        font-size: 20px;
        color: #fff;
        border-bottom: 1px solid #ddd;
    }

    .ms-login {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 350px;
        margin: -190px 0 0 -175px;
        border-radius: 5px;
        background: rgba(19, 19, 23, 0.3);
        overflow: hidden;
    }

    .ms-content {
        padding: 30px 30px;
    }

    .login-btn {
        text-align: center;
    }

    .login-btn button {
        width: 100%;
        height: 36px;
        margin-bottom: 10px;
    }

    .login-tips {
        font-size: 12px;
        line-height: 30px;
        color: #fff;
    }
</style>

<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 人员管理
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="searchData">
                <el-row type="flex" class="row-bg" justify="space-between">
                    <div>
                        <el-button
                                type="primary"
                                icon="el-icon-edit"
                                @click="handleAdd()"
                                class="handle-box"
                        >增加
                        </el-button>
                    </div>
                    <div type="flex" class="row-bg" justify="end">
                        <el-form-item>
                            <el-input v-model="searchData.username" clearable placeholder="姓名" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.email" clearable placeholder="邮箱" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.phone" clearable placeholder="手机号" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
            >
                <!--            <el-table-column fixed width="50" type="selection" align="center"></el-table-column>-->
                <el-table-column width="50" type="index" label="序号" align="center"></el-table-column>
                <af-table-column prop="username" label="姓名" align="center"></af-table-column>
                <af-table-column prop="email" label="邮箱" align="center"></af-table-column>
                <af-table-column prop="phone" label="手机号" align="center"></af-table-column>
                <af-table-column prop="gender" label="性别" align="center" :formatter="formatSex"></af-table-column>
                <af-table-column prop="remark" label="备注" align="center"></af-table-column>
                <af-table-column prop="update_time" label=" 更新时间 " align="center" :formatter="dateFormat"></af-table-column>
                <el-table-column fixed="right" label="操作" width="150" align="center">
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
                                class="red"
                                @click="handledelete(scope.row)"
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
        <el-dialog :title="makeTitle" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :rules="rules" :model="form" label-width="100px">
                <el-form-item label="名称" prop="username">
                    <el-input v-model="form.username"></el-input>
                </el-form-item>
                <el-form-item label="邮箱" prop="email">
                    <el-input v-model="form.email"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="form.phone"></el-input>
                </el-form-item>
                <el-form-item label="性别" prop="gender">
                    <el-select style="width:100%" v-model="form.gender" placeholder="请选择类型">
                        <el-option
                                v-for="item in genderOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.remark"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {validateEMail, validatePhoneTwo} from '../../../util/validate'
    export default {
        name: "staff",
        data() {
            return{
                tableData: [],
                editVisible: false,
                form: {remark: ''},
                id: -1,
                staffData: [],
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                searchData: {
                    username: "",
                    phone: "",
                    email: ""
                },
                makeTitle: '',
                genderOptions: [
                    {"label": "男",
                    "value":'male'},
                    {'label': "女",
                    "value": "female"}
                ],
                rules: {
                    username: [
                        {required: true, message: '请输入姓名'},
                        {trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: '请输入邮箱'},
                        {validator: validateEMail, trigger: 'blur'}
                    ],
                    phone: [
                        {required: true, message: "请输入手机号"},
                        {validator: validatePhoneTwo, trigger: 'blur'}
                    ],
                    gender: [
                        {required: true, message: "请输入性别"},
                        {trigger: 'blur'}
                    ]
                },
                loading: true
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.$http.get( `asset/api/staff/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&username=${this.searchData.username}&phone=${
                    this.searchData.phone}&email=${this.searchData.email}`, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data))
                    this.loading = false
                });
            },
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.makeTitle = "编辑";
                this.form = JSON.parse( JSON.stringify(row));
                console.log(this.form)
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    if(this.makeTitle=="增加"){
                        this.$http.post( `asset/api/staff/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("保存成功")
                            this.searchData = {
                                username: "",
                                    phone: "",
                                    email: ""
                            },
                            this.form = {};
                            this.getData()
                        }).catch( (error) => {
                            this.$message.error(JSON.stringify(error.response.data))
                        })
                    }else{
                        this.$http.put( `asset/api/staff/${this.id}/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("修改成功")
                            this.getData()
                        }).catch( (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },
            //新增弹框
            handleAdd() {
                this.form = {};
                this.makeTitle = "增加";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            //查询工作人员信息
            querystaff() {
                this.$http.get( `asset/api/staff/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.staffData = res.data
                })
            },
            //分页
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            handledelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.delete( `asset/api/staff/${row.id}`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex', 1)
                        this.getData()
                    } else {
                        this.$message.error('删除失败！');
                    }

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data))
                });
                })},

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
            //处理性别
            formatSex(row) {
                return row.gender == 'male' ? '男' : row.gender == 'female' ? '女':"未知";
            },
        },
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .red {
        color: #ff0000;
    }

    .handle-box {
        margin-bottom: 20px;
    }

    .handle-input {
        width: 200px;
        display: inline-block;
    }
    .table-width {
        word-break: keep-all;
        white-space: nowrap;
    }
    .el-upload--text {
        border:none
    }


</style>

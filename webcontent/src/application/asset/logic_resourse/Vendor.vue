<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 供应商
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
                            <el-input v-model="searchData.vendor_name" clearable placeholder="供应商名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.contact" clearable placeholder="联系人" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.phone" clearable placeholder="电话" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.email" clearable placeholder="邮箱" class="handle-input"></el-input>
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
                <af-table-column prop="vendor_name" label="名称" align="center"></af-table-column>
                <af-table-column prop="address" label="地址" align="center"></af-table-column>
                <af-table-column prop="contact" label="联系人" align="center"></af-table-column>
                <af-table-column prop="phone" label="电话" align="center"></af-table-column>
                <af-table-column prop="email" label="邮箱" align="center"></af-table-column>
                <af-table-column prop="main_products" label="产品说明" align="center"></af-table-column>
                <af-table-column prop="sign_up_time" label="成立时间" align="center"></af-table-column>
                <af-table-column prop="enterprise_type" label="企业类型" align="center"></af-table-column>
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
        <el-dialog :title="makeTitle" :visible.sync="editVisible" width="50%">
            <el-form ref="form" :rules="rules" :model="form" label-width="85px">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="名称" prop="vendor_name">
                            <el-input v-model="form.vendor_name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="地址" prop="address">
                            <el-input v-model="form.address"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="联系人" prop="contact">
                            <el-input v-model="form.contact"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="电话" prop="phone">
                            <el-input v-model="form.phone"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="邮箱" prop="email">
                            <el-input v-model="form.email"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="产品说明">
                            <el-input v-model="form.main_products"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="成立时间">
                            <el-date-picker
                                    v-model="form.sign_up_time"
                                    type="date"
                                    placeholder="选择日期"
                                    :editable="false"
                                    style="width: 100%"
                                    value-format=yyyy-MM-dd>
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="企业类型">
                            <el-select style="width:100%" v-model="form.enterprise_type" placeholder="请选择企业类型">
                                <el-option
                                        v-for="item in typeOptions"
                                        :key="item.value"
                                        :label="item.value"
                                        :value="item.value">
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="备注">
                            <el-input type="textarea" v-model="form.remark"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {validatePhoneTwo, validateEMail} from  '../../../util/validate'
    export default {
        name: "staff",
        data() {
            return{
                tableData: [],
                editVisible: false,
                form: {},
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
                    vendor_name: "",
                    contact: "",
                    phone: "",
                    email: ""
                },
                makeTitle: '',
                typeOptions:[{
                    value: "合资"
                },{
                    value: "独资"
                },{
                    value: "国有"
                },{
                    value: "私营"
                },{
                    value: "全民所有制"
                },{
                    value: "集体所有制"
                },{
                    value: "股份制"
                },{
                    value: "有限责任"
                }],
                rules: {
                    vendor_name: [
                        {required: true, message: "请输入厂商名称"},
                        {trigger: 'blur'}
                    ],
                    address: [
                        {required: true, message: "请输入厂商地址"},
                        {trigger: 'blur'}
                    ],
                    contact: [
                        {required: true, message: '请输入联系人'},
                        {trigger: 'blur'}
                    ],
                    phone: [
                        {required: true, message: '请输入联系方式'},
                        {validator: validatePhoneTwo, trigger: 'blur'}
                    ],
                    email: [
                        {required: true, message: "请输入邮箱"},
                        {validator: validateEMail, trigger: 'blur'}
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
                this.$http.get( `asset/api/vendor/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&vendor_name=${this.searchData.vendor_name}&contact=${this.searchData.contact
                }&phone=${this.searchData.phone}&email=${this.searchData.email}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                }).catch( (error) => {
                    console.log('失败==' + error);
                    this.$message.error(error);
                    this.loading = false
                });
            },
            // 编辑操作
            handleEdit(row) {

                this.id = row.id;
                this.makeTitle = "编辑";
                this.form = JSON.parse( JSON.stringify(row));
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
                        this.$http.post( `asset/api/vendor/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false;
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("保存成功");
                            this.form = {};
                            this.searchData = {
                                vendor_name: "",
                                    contact: "",
                                    phone: "",
                                    email: ""
                            };
                            this.getData();
                        }).catch( (error) => {
                            console.log('Error' + error.response);
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                    }else{
                        this.$http.put(`asset/api/vendor/${this.id}/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false;
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("修改成功");
                            this.getData();
                        }).catch( (error) =>{
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
                this.form = {}
                this.makeTitle = "增加";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
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
                }).then(() => {this.$http.delete( `asset/api/vendor/${row.id}`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex', 1)
                        this.getData()
                    } else {
                        this.$message.error(res.data.msg);
                    }

                }).catch( (error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
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
            //验证手机号
            animate(){
                var re = /^1\d{10}$/;
                let str = this.form.phone;
                if(re.test(str)){
                    this.phoneValue = 0
                    console.log('成功');
                }else {
                    this.phoneValue = 1;
                    this.$message.success('手机号格式错误！');
                }
            }
        },
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve";
    .red {
        color: #ff0000;
    }

    .handle-box {
        margin-bottom: 20px;
    }

    .table-width {
        word-break: keep-all;
        white-space: nowrap;
    }
    .el-upload--text {
        /*cursor: pointer;*/
        /*position: relative;*/
        /*overflow: hidden;*/
        border:none
    }


</style>

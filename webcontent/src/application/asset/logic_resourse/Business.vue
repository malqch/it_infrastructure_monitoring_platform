<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 业务
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
                            <el-input v-model="searchData.name" clearable placeholder="名称" class="handle-input"></el-input>
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
                <af-table-column prop="name" label="名称" align="center"></af-table-column>
                <af-table-column prop="remark" label="备注" align="center"></af-table-column>
                <af-table-column prop="staff" label="工作人员" align="center" >
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchStaff(scope.$index)" class="color-link">查看负责人信息</el-link>
                    </template>
                </af-table-column>
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
            <el-form ref="form" :rules="rules" :model="form" label-width="60px">
                <el-form-item label="名称" prop="name">
                    <el-input v-model="form.name"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.remark"></el-input>
                </el-form-item>
                <el-form-item label="负责人">
                    <el-select style="width:100%" value-key="id"  v-model="form.staff" placeholder="请选择负责人" @focus="querystaff()" clearable>
                        <el-option v-for="item in staffData"
                                   :key=item.username
                                   :label="item.username"
                                   :value=item.id>
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="负责人信息" :visible.sync="staffVisible" width="30%" class="alert_dialog">
            <ul :model="staffDataRes" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">负责人:</label>
                    <span class="network_span">{{staffDataRes.username}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">邮箱:</label>
                    <span class="network_span">{{staffDataRes.email}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">电话:</label>
                    <span class="network_span">{{staffDataRes.phone}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">备注:</label>
                    <span class="network_span">{{staffDataRes.remark}}</span>
                </li>
            </ul>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "server",
        data() {
            return{
                tableData: [],
                editVisible: false,
                staffVisible: false,
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
                    name: ""
                },
                makeTitle: '',
                staffDataRes: {"username": "", "email": "", "phone": ""},
                staffObject: "",
                rules: {
                    name: [{required: true, message: '请输入业务名'}, {trigger: 'blur'}]
                },
                loading: true
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.$http.get( `asset/api/business/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&name=${this.searchData.name}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                }).catch( (error) =>{
                    console.log('失败==' + error);
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false
                });
            },
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.makeTitle = "编辑";
                this.form = JSON.parse( JSON.stringify(row));
                if(row['staff']) {
                    this.staffObject = row.staff
                    this.form.staff = row.staff.username
                }
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
                        this.$http.post( `asset/api/business/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success(res.data.msg)
                            this.form = {};
                            this.searchData = {
                                name: ""
                            };
                            this.getData()
                        }).catch( (error) =>{
                            console.log('Error' + error.response);
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }else{
                        // staff 存在
                        if(this.form.staff && typeof this.form.staff != 'number'){
                            this.$set(this.form, 'staff', this.staffObject.id)
                        }
                        this.$http.put( `asset/api/business/${this.id}/`,{'id':this.form.id,'name': this.form.name,
                            'remark': this.form.remark, "staff": this.form.staff},{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success(res.data.msg)
                            this.getData()
                        }).catch( (error) => {
                            console.log('Error' + error.response);
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
            searchStaff(index) {
                if(this.tableData[index]["staff"]!=null){
                    this.staffDataRes = this.tableData[index]["staff"];
                    this.staffVisible = true;
                }else{
                    this.$message.success("负责人信息不存在")
                }
            },
            handledelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.delete( `asset/api/business/${row.id}`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex', 1)
                        this.getData()
                    }  else {
                        console.log(res)
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
            }
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
        /*cursor: pointer;*/
        /*position: relative;*/
        /*overflow: hidden;*/
        border:none
    }


</style>

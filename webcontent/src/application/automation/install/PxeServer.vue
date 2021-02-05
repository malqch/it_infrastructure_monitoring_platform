<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> pxe管理
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
                            <el-input v-model="searchData.pxe_name" placeholder="名称" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.pxe_server_ip" placeholder="ip" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </div>
                </el-row>
            </el-form>
            <el-table
                    v-loading="loading"
                    ref="table"
                    :data="tableData"
                    border
                    style="width: 100%"
                    @expand-change="queryPxeos"
            >
                <el-table-column type="expand">
                    <template slot-scope="scope">
                        <el-table v-loading="osloading" ref="ostable" :data="scope.row.ruleItemData" border stripe style="width: 100%">
                            <el-table-column prop="os_name" label="os名称" align="center"></el-table-column>
                            <el-table-column prop="os_version" label="os版本" align="center"></el-table-column>
                            <el-table-column prop="ks_name" label="ks_name" align="center"></el-table-column>
                            <el-table-column prop="profile" label="profile" align="center" width="150px"></el-table-column>
                            <el-table-column prop="ifenable" label="ifenable" align="center"></el-table-column>
                            <el-table-column prop="type" label="type" align="center"></el-table-column>
                            <el-table-column prop="ks_content" label="ks_content" align="center" width="120px">
                                <template slot-scope="scope">
                                    <el-button @click="querykscontent(scope.row)">查看ks文件</el-button>
                                </template>
                            </el-table-column>
                            <el-table-column prop="create_time" label="create_time" align="center" :formatter="datetimeFormat" width="120px"></el-table-column>
                            <el-table-column fixed="right" label="操作" width="120" align="center">
                                <template slot-scope="osscope">
                                    <el-button
                                            type="text"
                                            icon="el-icon-edit"
                                            @click="handleosEdit(scope.row, osscope.row)"
                                    >编辑
                                    </el-button>
                                    <el-button
                                            type="text"
                                            icon="el-icon-delete"
                                            class="red"
                                            @click="handleosdelete(scope.row, osscope.row)"
                                    >删除
                                    </el-button>
                                </template>
                            </el-table-column>
                        </el-table>
                    </template>
                </el-table-column>
                <el-table-column prop="pxe_name" label="pxe_name" align="center"></el-table-column>
                <el-table-column prop="pxe_server_ip" label="pxe_server_ip" align="center"></el-table-column>
                <el-table-column prop="ipmi_server_ip" label="ipmi_server_ip" align="center"></el-table-column>
                <el-table-column prop="ifenable" label="ifenable" align="center"></el-table-column>
                <el-table-column prop="device_usage" label="usage" align="center"></el-table-column>
                <el-table-column prop="remark" label="备注" align="center"></el-table-column>
                <el-table-column prop="create_time" label=" 创建时间 " align="center" :formatter="datetimeFormat"></el-table-column>
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
<!--        编辑pxe-->
        <el-dialog :title="makeTitle" :visible.sync="editVisible" width="30%">
            <el-form ref="form" :rules="rules" :model="form" label-width="130px">
                <el-form-item label="pxe_name" prop="pxe_name">
                    <el-input v-model="form.pxe_name" clearable></el-input>
                </el-form-item>
                <el-form-item label="pxe_server_ip" prop="pxe_server_ip">
                    <el-input v-model="form.pxe_server_ip" clearable></el-input>
                </el-form-item>
                <el-form-item label="ipmi_server_ip" prop="ipmi_server_ip">
                    <el-input v-model="form.ipmi_server_ip" clearable></el-input>
                </el-form-item>
                <el-form-item label="ifenable">
                    <el-select style="width:100%" v-model="form.ifenable" placeholder="请选择是否启用" clearable>
                        <el-option
                                v-for="item in typeifenable"
                                :key="item.value"
                                :label="item.value"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="usage">
                    <el-input v-model="form.device_usage" clearable></el-input>
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
<!--        编辑os-->
        <el-dialog :title="makeosTitle" :visible.sync="editosVisible" width="30%">
            <el-form ref="osform" :model="osform" label-width="100px">
                <el-form-item label="os_name">
                    <el-input v-model="osform.os_name"></el-input>
                </el-form-item>
                <el-form-item label="os_version">
                    <el-input v-model="osform.os_version"></el-input>
                </el-form-item>
                <el-form-item label="ks_name">
                    <el-input v-model="osform.ks_name"></el-input>
                </el-form-item>
                <el-form-item label="profile">
                    <el-input v-model="osform.profile"></el-input>
                </el-form-item>
                <el-form-item label="type">
                    <el-select style="width:100%" v-model="osform.type" placeholder="请选择类型" clearable>
                        <el-option
                                v-for="item in typeData"
                                :key="item.value"
                                :label="item.value"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="ifenable">
                    <el-select style="width:100%" v-model="osform.ifenable" placeholder="请选择是否启用" clearable>
                        <el-option
                                v-for="item in typeifenable"
                                :key="item.value"
                                :label="item.value"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="ks_content">
                    <el-input type="textarea" v-model="osform.ks_content"></el-input>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editosVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveosEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import {datetimeFormat} from '../../../util/formatData'

    export default {
        name: "pxeserver",
        data() {
            return{
                tableData: [],
                editVisible: false,
                form: {},
                id: -1,
                os_id: -1,
                staffData: [],
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                searchData: {
                    pxe_name: "",
                    pxe_server_ip: ""
                },
                makeTitle: '',
                typeifenable:[{
                    value: "enabled"
                },{
                    value: "disabled"
                }],
                pxeosData: [],
                osform: {},
                makeosTitle: "",
                editosVisible: false,
                pxeData: [],
                typeData: [{
                    value: 'suse'
                }, {
                    value: "rhel"
                }, {
                    value: "neokylin"
                }, {
                   value: "exit"
                }],
                kscontentVisible: false,
                ksContentData: "",
                pxe_server_id: 1,
                datetimeFormat: null,
                rules: {
                    pxe_name: [
                        {required: true, message: '请输入名称'},
                        {trigger: 'blur'}
                    ],
                    pxe_server_ip: [
                        {required: true, message: '请输入pxe server的ip'},
                        {trigger: 'blur'}
                    ],
                    ipmi_server_ip: [
                        {required: true, message: '请输入ipmi server的ip'},
                        {trigger: 'blur'}
                    ]
                },
                loading: true,
                osloading: false,
            }
        },
        created() {
            this.getData();
            this.datetimeFormat=datetimeFormat
        },
        methods: {
            getData() {
                this.$http.get( `automation/api/pxe_server/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&pxe_name=${this.searchData.pxe_name}&pxe_server_ip=${this.searchData.pxe_server_ip
                }`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        console.log(res.data['data'])
                    res.data['data'] && res.data['data'].map(item => {
                        item.ruleItemData = [];
                    });
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                    console.log(this.tableData)
                }).catch((error) => {
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
                this.editVisible = true;
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    if(this.makeTitle=="增加"){
                        this.$http.post( `automation/api/pxe_server/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("保存成功")
                            this.form = {};
                            this.getData()
                        }).catch((error) => {
                            console.log('Error' + error.response);
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }else{
                        this.$http.put( `automation/api/pxe_server/${this.id}/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success("修改成功")
                            this.getData()
                        }).catch((error) => {
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
                this.form = {}
                this.makeTitle = "增加";
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            handleosEdit(row, osrow) {
                this.os_id = osrow.id;
                this.makeosTitle = "编辑";
                this.pxe_server_id = row.id
                this.osform = JSON.parse( JSON.stringify(osrow));
                this.editosVisible = true;
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
                }).then(() => {this.$http.delete( `automation/api/pxe_server/${row.id}`,  {
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

                }).catch((error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},

            //处理时间格式
            // dateFormat(row, column){
            //     const daterc = row[column.property]
            //     if(daterc!=null){
            //         const dateMat = new Date(daterc);
            //         const year = dateMat.getFullYear();
            //         const month = dateMat.getMonth() + 1;
            //         const day = dateMat.getDate();
            //         const hh = dateMat.getHours();
            //         const mm = dateMat.getMinutes();
            //         const ss = dateMat.getSeconds();
            //         const timeFormat = year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
            //         return timeFormat;
            //     }
            // },
            querypxeserveros() {
                this.$http.get(`automation/api/pxe_server_os/?pxe_server_id=${this.osform.pxe_server_id}`, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    // 遍历当前页面表
                    this.tableData.forEach((temp, index) => {
                        // 找到当前点击的行，把动态获取到的数据赋值进去
                        if (temp.id === this.pxe_server_id) {
                            this.tableData[index].ruleItemData = res.data;
                            console.log(this.tableData)
                        }
                    });
                });
            },
            // 点击展开行时的查询
            queryPxeos(row, expandedRows) {
                // 该处是用于判断是展开还是收起行，只有展开的时候做请求，避免多次请求！
                // 展开的时候expandedRows有值，收起的时候为空.
                if (expandedRows.length > 0) {
                    this.osloading = true
                    this.$http.get(`automation/api/pxe_server_os/?pxe_server_id=${row.id}`, {
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        // 遍历当前页面表
                        this.tableData.forEach((temp, index) => {
                            // 找到当前点击的行，把动态获取到的数据赋值进去
                            if (temp.id === row.id) {
                                this.tableData[index].ruleItemData = res.data;
                            }
                        });
                        this.osloading = false
                    });
                }
            },
            queryPxeserver() {
                this.$http.get( `automation/api/pxe_server/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.pxeData = res.data
                }).catch((error) => {
                    console.log('失败==' + error);
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 保存编辑
            saveosEdit() {
                if(this.makeosTitle=="增加"){
                    this.$http.post( `automation/api/pxe_server_os/`,this.osform,{
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.editosVisible = false
                        console.log('Response:' + JSON.stringify(res));
                        this.$message.success("保存成功")
                        this.querypxeserveros()
                    }).catch((error) => {
                        console.log('Error' + error.response);
                        this.$message.error(JSON.stringify(error.response.data));
                    })
                }else{
                    this.$http.put( `automation/api/pxe_server_os/${this.os_id}/`,this.osform,{
                        headers:{
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.editosVisible = false
                        console.log('Response:' + JSON.stringify(res));
                        this.$message.success("修改成功")
                        this.querypxeserveros()
                    }).catch((error) => {
                        console.log('Error' + error.response);
                        this.$message.error(JSON.stringify(error.response.data));
                    })
                }
            },
            // 查看ks文件
            querykscontent(row) {
                this.$alert(row.ks_content, 'ks_content', {
                    confirmButtonText: '取消',
                    customClass: 'message-logout'
                });

            },
            //删除os
            handleosdelete(row, osrow) {
                this.pxe_server_id = row.id
                this.osform = {"pxe_server_id": row.id}
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.delete( `automation/api/pxe_server_os/${osrow.id}`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.querypxeserveros()
                    } else {
                        this.$message.error('删除失败！');
                    }

                }).catch((error) => {
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })
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
        border:none
    }


</style>
<style>
    .message-logout{
        width:675px;
        padding:0px 15px 15px 20px;
    }
    .message-logout .el-message-box__content{
        height: 450px;
        overflow: auto;
    }
    .message-logout .el-message-box__title{
        color:#409EFF;
    }
</style>

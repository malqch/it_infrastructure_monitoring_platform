<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 文档管理
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
                            <el-input v-model="searchData.contract_name" clearable placeholder="名称" class="handle-input"></el-input>
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
                <af-table-column prop="contract_name" label="名称" align="center"></af-table-column>
                <af-table-column prop="sign_time" label="签署时间" align="center"></af-table-column>
                <af-table-column prop="remark" label=" 备注 " align="center"></af-table-column>
                <af-table-column prop="update_time" label=" 更新时间 " align="center" :formatter="dateFormat"></af-table-column>
                <el-table-column label="文档附件" align="center" width="150">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-download"
                                class="colo-green"
                                @click="downloadcontract(scope.row)"
                        >下载文档
                        </el-button>
                    </template>
                </el-table-column>
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
                <el-form-item label="签署时间" prop="sign_time">
                    <el-date-picker
                            v-model="form.sign_time"
                            type="date"
                            placeholder="选择日期"
                            :editable="false"
                            style="width: 100%"
                            value-format=yyyy-MM-dd>
                    </el-date-picker>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input type="textarea" v-model="form.remark"></el-input>
                </el-form-item>
                <el-form-item label="文件名">
                    <el-input v-model="filename" disabled></el-input>
                </el-form-item>
                <el-upload
                        class="upload-demo"
                        ref="uploadFile"
                        action="no"
                        :limit="1"
                        :on-change="fileChange"
                        :auto-upload="false">
                    <el-button slot="trigger" size="small" type="warning" plain>选取文档</el-button>
                    <div slot="tip" class="el-upload__tip"></div>
                </el-upload>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "staff",
        data() {
            return{
                tableData: [],
                editVisible: false,
                form:{},
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
                    contract_name: ""
                },
                makeTitle: '',
                headers:{
                    'username': 'admin',
                    'password': '111111'
                },
                uploadData: {},
                file: "",
                filename: "",
                contractVisble:false,
                contractData: "",
                result: [],
                rules: {
                    sign_time: [
                        {required: true, message: "请输入签署时间"},
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
                this.$http.get( `asset/api/contract/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&contract_name=${this.searchData.contract_name}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                }).catch( (error) => {
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
                this.filename = row.contract_name;
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    const formdata = new FormData()
                    formdata.append("sign_time", this.form.sign_time);
                    formdata.append('file', this.file);
                    if(this.form.remark!=undefined){
                        formdata.append('remark', this.form.remark);
                    }
                    formdata.append('contract_name', this.filename)
                    if(this.makeTitle=="增加"){
                        this.$http.post( `asset/api/contract/`,formdata,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            if(res.status===202){
                                this.$message.error('文件名重复，请检查是否为同一文件')
                            }else{
                                this.$message.success("保存成功")
                                this.editVisible = false
                                console.log('Response:' + JSON.stringify(res));
                                this.form = {};
                                this.searchData = {
                                    contract_name: ""
                                };
                                this.getData()
                                this.$refs.uploadFile.clearFiles();
                                this.filename = ''
                            }
                        }).catch( (error) =>{
                            console.log('Error' + error.response);
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }else{
                        this.$http.put( `asset/api/contract/${this.id}/`,formdata,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            if(res.status===202){
                                this.$message.error('文件名重复，请检查是否为同一文件')
                            }else{
                                this.$message.success("修改成功")
                                this.editVisible = false
                                console.log('Response:' + JSON.stringify(res));
                                this.getData();
                                this.$refs.uploadFile.clearFiles();
                                this.filename = ''
                            }
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
                this.filename = '';
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                    this.$refs.uploadFile.clearFiles();
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
                }).then(() => {this.$http.delete( `asset/api/contract/${row.id}`,  {
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
            // 获得文件和文件名
            fileChange(file) {
                this.file = file.raw
                this.filename = file.name
            },
            //下载合同
            downloadcontract(row) {
                this.$http.post(`asset/api/contract/download/`,{"contract_name": row.contract_name},{
                    headers:{
                        'token': localStorage.getItem('token')
                    },responseType: 'blob',
                }).then((res) => {
                    let data = res.data
                    var result = {}
                    try {
                        let unit8Arr = new Uint8Array(data)
                        let encodedStr = String.fromCharCode.apply(null, unit8Arr)
                        //将乱码的中文进行转换
                        let decodedStr = decodeURIComponent(escape((encodedStr)))
                        result = JSON.parse(decodedStr)
                    } catch (e) {
                        console.error(e)
                    }
                    if (!result && !result.isSuccess) {
                        this.$Message.error(result.resultMsg)
                    } else {
                        var newBlob = new Blob([data], {type: 'text/plain;charset=UTF-8'})
                        var anchor = document.createElement('a')
                        anchor.download = row.contract_name
                        anchor.href = window.URL.createObjectURL(newBlob)
                        anchor.click()
                    }
                }).catch(function (err) {
                    console.log(err)
                })
            }
        },
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .red {
        color: #ff0000;
    }
    .colo-green{
        color:#67C23A;
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
    .upload-demo {
        padding-left: 100px;
    }


</style>

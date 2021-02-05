<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 端口检查
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true">
                <el-row class="margin_bot">
                    <el-row>
                        <el-col :span="2">
                            <el-button class="mr10" @click="exportTemplate" type="info" plain>下载模版
                            </el-button>
                        </el-col>
                        <el-col :span="18">
                            <el-upload
                                    class="upload-demo inlineB"
                                    ref="uploadExcel"
                                    action="no"
                                    :limit="1"
                                    :on-change="fileChange"
                                    :auto-upload="false">
                                <el-button class="mr10" slot="trigger" size="small" type="warning" plain>选择文件</el-button>
                                <div slot="tip" class="el-upload__tip"></div>
                            </el-upload>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="18">
                            <el-form-item label="pxe_server">
                                <el-select style="width:450px" value-key="id"  v-model="pxe_server_id" placeholder="请选择pxe server" @focus="queryPxeserver" clearable>
                                    <el-option v-for="item in pxeData"
                                               :key=item.id
                                               :label="`name:${item.pxe_name} ip:${item.pxe_server_ip} 用途:${item.device_usage}`"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="2">
                            <el-button type="primary" @click="uploadExcel">添加</el-button>
                        </el-col>
                        <el-col :span="2">
                            <el-button type="primary" @click="addjobcheck">创建</el-button>
                        </el-col>
                    </el-row>
                </el-row>
            </el-form>
            <el-table
                    :data="tableData"
                    border
                    ref="table"
                    style="width: 100%"
                    :row-key="getRowKeys"
                    @selection-change="selectionChange"
            >
                <el-table-column fixed width="50" type="selection" align="center" :reserve-selection="true" ></el-table-column>
                <af-table-column prop="hostname" label="主机名" align="center"></af-table-column>
                <af-table-column prop="usage" label="用途" align="center"></af-table-column>
                <af-table-column prop="manage_address" label="console_ip" align="center"></af-table-column>
                <af-table-column prop="device_sn" label="sn" align="center"></af-table-column>
                <af-table-column prop="pxe_server_ip" label="pxe_server_ip" align="center"></af-table-column>
                <af-table-column prop="ipmi_server_ip" label="ipmi_server_ip" align="center"></af-table-column>
                <af-table-column prop="location_zone" label="location" align="center"></af-table-column>
                <el-table-column fixed="right" label="操作" width="200" align="center">
                    <template slot-scope="scope">
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
        </div>
    </div>
</template>

<script>
    export default {
        name: "JobCheck",
        data() {
            return{
                tableData: [],
                pxeData: [],
                pxe_server_id: "",
                file: "",
                filename: "",
                checkList: [],
            }
        },
        methods: {
            //查询pxe信息
            queryPxeserver() {
                this.$http.get( `automation/api/pxe_server/?ifenable=enabled`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.pxeData = res.data
                }).catch((error) => {
                    console.log('失败==' + error);
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 获得文件和文件名
            fileChange(file) {
                this.file = file.raw
                this.filename = file.name
            },
            // 上传excel,调用后台
            uploadExcel() {
                const formdata = new FormData()
                formdata.append("pxe_server_id", this.pxe_server_id);
                formdata.append('file', this.file);
                formdata.append('file_name', this.filename)
                this.$http.post( `automation/api/pxe_server/upload_excel/`,formdata,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data
                    console.log('Response:' + JSON.stringify(res));
                }).catch( (error) =>{
                    console.log('Error' + error.response);
                    this.$message.error(JSON.stringify(error.response.data));
                })
            },
            //获得row-key
            getRowKeys(row) {
                return row.hostname;
            },
            selectionChange(row){
                this.checkList = row
            },
            handledelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {
                    this.tableData.some((item,i)=>{
                        if(item.hostname == row.hostname){
                            this.tableData.splice(i,1);
                            console.log(this.tableData)
                            return true;
                        }
                    });
                    this.checkList.some((item,i)=>{
                        if(item.hostname == row.hostname){
                            this.checkList.splice(i,1);
                            console.log(this.tableData)
                            return true;
                        }
                    })
                })},

            // 导出模版
            exportTemplate() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["hostname"];// 上面设置Excel的表格第一行的标题

                    const list = []
                    export_json_to_excel(tHeader, list, "端口检查模版");   //标题，数据，文件名
                });
            },
            addjobcheck() {
                this.$http.post( `automation/api/job_check/`, this.checkList,{
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.$message.success(res.data['msg'])
                    this.$refs.uploadExcel.clearFiles();
                    this.tableData = []
                    this.pxe_server_id = ''
                    this.file = ''
                    this.file_name = ''
                }).catch( (error) => {
                    console.log('失败==' + error);
                    this.$message.error(JSON.stringify(error.response.data));
                });
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
    .margin_bot{
        margin-bottom: 10px;
    }


</style>
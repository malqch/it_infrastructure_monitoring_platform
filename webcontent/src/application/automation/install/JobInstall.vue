<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 物理机装机
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
                        <el-col :span="8">
                            <el-form-item label="pxe_server" >
                                <el-select value-key="id"  v-model="pxe_server_id" placeholder="请选择pxe server" @focus="queryPxeserver" clearable class="handle-input">
                                    <el-option v-for="item in pxeData"
                                               :key=item.id
                                               :label="`name:${item.pxe_name} ip:${item.pxe_server_ip} 用途:${item.device_usage}`"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="7">
                            <el-form-item label="os">
                                <el-select value-key="id"  v-model="os_id" placeholder="请选择os" @focus="queryPxeserveros" clearable class="handle-input">
                                    <el-option v-for="item in osData"
                                               :key=item.id
                                               :label="`name:${item.os_name} version:${item.os_version}`"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="5">
                            <el-form-item label="用途">
                                <el-input v-model="usage" clearable ></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="3">
                            <el-button type="primary" @click="uploadExcel">添加</el-button>
                            <el-button type="primary" @click="addjobinstall">创建</el-button>
                        </el-col>
                    </el-row>
                    <el-row v-show="isShowSwitch">
                        <el-row>
                            <el-form-item label="switch">
                                <el-checkbox-group v-model="checkswitchList">
                                    <el-checkbox  v-for="item in switch_list"
                                                  :label="item"
                                                  :key="item">
                                        {{item}}
                                    </el-checkbox>
                                </el-checkbox-group>
                            </el-form-item>
                        </el-row>
                        <el-row>
                            <el-button type="primary" @click="matchmac">确 定</el-button>
                        </el-row>
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
                    :row-class-name="tableRowClassName"
            >
                <el-table-column fixed width="50" type="selection" align="center" :selectable="selecttable"></el-table-column>
                <af-table-column prop="ip" label="ip" align="center"></af-table-column>
                <af-table-column prop="device_netmask" label="netmask" align="center"></af-table-column>
                <af-table-column prop="device_gateway" label="gateway" align="center"></af-table-column>
                <af-table-column prop="hostname" label="主机名" align="center"></af-table-column>
                <af-table-column prop="usage" label="usage" align="center"></af-table-column>
                <af-table-column prop="manage_address" label="console_ip" align="center"></af-table-column>
                <af-table-column prop="device_sn" label="sn" align="center"></af-table-column>
                <af-table-column prop="pxe_server_ip" label="pxe_server_ip" align="center"></af-table-column>
                <af-table-column prop="ipmi_server_ip" label="ipmi_server_ip" align="center"></af-table-column>
                <af-table-column prop="os_name" label="os_name" align="center"></af-table-column>
                <af-table-column prop="os_version" label="os_version" align="center"></af-table-column>
                <af-table-column prop="status" label="status" align="center" :formatter="formatStatus"></af-table-column>
                <el-table-column prop="mac" label="mac" width="150px" align="center">
                    <template slot-scope="scope">
                        <div v-for="(item,index) in scope.row.mac" :key="index">
                           {{item}}&nbsp;&nbsp;&nbsp;
                        </div>
                        <el-button
                                type="text"
                                icon="el-icon-edit"
                                class="red"
                                @click="handleEdit(scope.row, scope.$index)"
                        >编辑
                        </el-button>
                    </template>
                </el-table-column>
                <el-table-column fixed="right" label="操作" width="100" align="center">
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
        <el-dialog title="修改mac" :visible.sync="editVisible" width="30%" class="alert_dialog">
            <el-form ref="all_mac_list" :model="all_mac_list" label-width="70px">
                <el-form-item label="mac">
                    <el-checkbox-group v-model="checkmacList">
                        <el-checkbox  v-for="item in all_mac_list"
                                      :label="item"
                                      :key="item">
                            {{item}}
                        </el-checkbox>
                    </el-checkbox-group>
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
    export default {
        name: "JobInstall",
        data() {
            return{
                tableData: [],
                pxeData: [],
                osData: [],
                pxe_server_id: "",
                os_id: "",
                usage: "",
                file: "",
                filename: "",
                checkList: [],
                select_color: false,
                checkswitchList: [],
                ports: [],
                switch_list: [],
                mac_list: [],
                ifname_list: [],
                all_mac_list: [],
                editVisible: false,
                checkmacList: [],
                index:0,
                isShowSwitch:false
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
            //查村pxe对应os
            queryPxeserveros() {
                if(this.pxe_server_id){
                    this.$http.get( `automation/api/pxe_server_os/?pxe_server_id=${this.pxe_server_id}&ifenable=enabled`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.osData = res.data
                    }).catch((error) => {
                        console.log('失败==' + error);
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else{
                    this.$message.error("请先选择pxe server")
                }
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
                formdata.append('os_id', this.os_id);
                formdata.append('usage', this.usage)
                this.$http.post( `automation/api/pxe_server/upload_excel/`,formdata,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data
                    console.log('Response:' + JSON.stringify(res));
                    const port_list = []
                    this.tableData.some((item)=>{
                        const mac_item_list = []
                        if(item.port){
                            item.port.some((port)=>{
                                port_list.push(port.switch)
                                mac_item_list.push(port.mac)
                            })
                        }
                        this.$set(item, 'mac_list', mac_item_list)
                        })

                    this.switch_list = Array.from(new Set(port_list))
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
                    })
                })},
            // 创建
            addjobinstall() {
                if(this.pxe_server_id=='' || this.os_id=='' || this.usage==''){
                    this.$message.warning('请把选项添加完整再创建！')
                }else{
                    this.isShowSwitch=true;
                    this.$http.post( `automation/api/job_install/`, this.checkList,{
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.$message.success(res.data['msg'])
                        this.$refs.uploadExcel.clearFiles();
                        this.tableData = []
                        this.usage = ''
                        this.os_id = ''
                        this.pxe_server_id = ''
                        this.file = ''
                        this.file_name = ''
                        this.checkswitchList = []
                        this.switch_list = []
                    }).catch( (error) => {
                        console.log('失败==' + error);
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }

            },
            // 导出模版
            exportTemplate() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["ip","hostname","netmask","gateway"];// 上面设置Excel的表格第一行的标题

                    const list = []
                    export_json_to_excel(tHeader, list, "装机模版");   //标题，数据，文件名
                });
            },
            //处理状态
            formatStatus(row) {
                return row.status == 10000 ? '端口检查成功' : row.status == '10001' ? '正在端口检查':row.status == '10002' ? '端口检查过期':row.status == '10003' ? '端口检查失败':row.status == '10004' ? '未端口检查':"未知";
            },
            //加条件判断是否可选
            selecttable(row) {
                if(row.status===10000){
                    return true;
                }else{
                    return false;
                }
            },
            //不能选择的加灰色
            tableRowClassName({row}) {
                if (row.status !== 10000) {
                    return 'select_color';
                }
                return ''
            },
            //根据选择的switch显示mac
            matchmac(){
                this.tableData.some((item)=>{
                    // this.all_mac_list = []
                    this.mac = []
                    this.ifname_list = []
                    if(item.port){
                        item.port.some((port)=>{
                            const index = this.checkswitchList.indexOf(port.switch)
                            if(index >= 0){
                                this.mac.push(port.mac)
                                this.ifname_list.push(port.ifname)
                            }
                        })
                    }
                    this.$set(item, 'mac', this.mac)
                    this.$set(item, 'ifname', this.ifname_list)
                })
                console.log(this.tableData)
            },
            //增加对mac地址编辑的弹框
            handleEdit(row, index){
                this.index = index
                this.editVisible = true
                this.all_mac_list = row.mac_list
                if(row.mac){
                    this.checkmacList = row.mac
                }else{
                    this.checkmacList = []
                }
            },
            //保存对mac地址的编辑
            saveEdit(){
                this.$set(this.tableData[this.index], 'mac', this.checkmacList)
                this.editVisible = false
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
        width: 305px;
        display: inline-block;
    }
    .table-width {
        word-break: keep-all;
        white-space: nowrap;
    }
    .margin_bot{
        margin-bottom: 10px;
    }
    /deep/ .el-table .select_color{
        color: #b9bdc3;
    }


</style>
<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 端口检查日志
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="searchData">
                <el-row>
                    <el-col :span="30" :inline="true">
                        <el-form-item>
                            <el-input v-model="searchData.device_name" placeholder="设备名" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.hostname" placeholder="主机名" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.sn" placeholder="sn" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.status" placeholder="状态" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.pxe_server_ip" placeholder="pxe_server_ip" class="handle-input" clearable></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="30" :inline="true">
                        <el-button @click="exportData" type="danger" plain>导出Excel
                        </el-button>
                    </el-col>
                </el-row>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    ref="table"
                    style="width: 100%"
            >
                <el-table-column type="expand">
                    <template slot-scope="scope">
                        <el-table ref="ostable" :data="scope.row.job_check" border stripe style="width: 100%">
                            <el-table-column prop="mac" label="mac" align="center"></el-table-column>
                            <el-table-column prop="switch" label="switch" align="center"></el-table-column>
                            <el-table-column prop="port" label="port" align="center"></el-table-column>
                            <el-table-column prop="ifname" label="ifname" align="center" width="150px"></el-table-column>
                            <el-table-column prop="vlan" label="vlan" align="center"></el-table-column>
                        </el-table>
                    </template>
                </el-table-column>


<!--                <el-table-column fixed width="50" type="selection" align="center" :reserve-selection="true" ></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <af-table-column prop="device_name" label="设备名" align="center"></af-table-column>
                <af-table-column prop="hostname" label="主机名" align="center"></af-table-column>
                <af-table-column prop="sn" label="sn" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center" width="100px"></af-table-column>
                <af-table-column prop="usage" label="用途" align="center"></af-table-column>
                <af-table-column prop="console_ip" label="console_ip" align="center"></af-table-column>
                <af-table-column prop="console_user" label="console_user" align="center"></af-table-column>
                <af-table-column prop="pxe_server_ip" label="pxe_server_ip" align="center"></af-table-column>
                <af-table-column prop="ipmi_server_ip" label="ipmi_server_ip" align="center"></af-table-column>
                <af-table-column prop="location" label="位置" align="center"></af-table-column>
                <af-table-column prop="update_time" label="更新时间" align="center" :formatter="dateFormat"></af-table-column>
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
    </div>
</template>

<script>
    export default {
        name: "JobCheckLog",
        data() {
            return {
                tableData: [],
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                searchData:{
                    pxe_server_ip: "",
                    device_name: "",
                    hostname: "",
                    sn: "",
                    status: ""
                },
                exportDataRes: [],
                job_check_length: 0,
                loading: true
            }
        },
        created() {
            this.getData()
        },
        methods: {
            getData(){
                this.$http.get( `automation/api/job_check/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&sn=${this.searchData.sn}&device_name=${this.searchData.device_name}&hostname=${
                    this.searchData.hostname}&pxe_server_ip=${this.searchData.pxe_server_ip}&status=${this.searchData.status}`, {
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
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
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
            //分页
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            // 导出数据
            exportData() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["设备名","主机名", "sn","status", "pxe_server_ip","ipmi_server_ip","位置","console_ip","console_user", "用途", "更新时间"];// 上面设置Excel的表格第一行的标题

                    const filterVal = ["device_name","hostname", "sn","status","pxe_server_ip", "ipmi_server_ip", "location", "console_ip", "console_user", "usage",
                        "update_time"]; // 上面的是tableData里对象的属性

                    this.$http.get(`automation/api/job_check/`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.exportDataRes = res.data;
                        console.log(this.exportDataRes)
                    }).then(() =>{
                        const list = this.exportDataRes;              //把data里的tableData存到list
                        const data = this.formatJson(filterVal, list);
                        console.log(data, 9999999)
                        const port_tHeader = ['mac', 'switch', 'port', 'ifname', 'vlan']
                        let port_obj=[];
                        for(let i=0;i<this.job_check_length;i++){
                            port_obj = port_obj.concat(port_tHeader)
                        }
                        console.log(port_obj)
                        const all_tHeader = tHeader.concat(port_obj)
                        export_json_to_excel(all_tHeader, data, "端口检查结果");   //标题，数据，文件名
                    })});
            },
            formatJson(filterVal, jsonData) {
                const data_list = []
                jsonData.map((v) => {
                    const res = filterVal.map(j => v[j])
                    const length = v.job_check.length
                    if(length > this.job_check_length){
                        this.job_check_length = length
                    }
                    const job_check_list = []
                    v.job_check.forEach(item =>{
                        job_check_list.push(item.mac)
                        job_check_list.push(item.switch)
                        job_check_list.push(item.port)
                        job_check_list.push(item.ifname)
                        job_check_list.push(item.vlan)
                    })
                    const results= res.concat(job_check_list)
                    data_list.push(results)
                });
                console.log(data_list, 7777777)
                return data_list
            },
        }
    }
</script>

<style scoped>

</style>

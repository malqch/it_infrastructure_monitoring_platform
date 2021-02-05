<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 装机日志
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
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    ref="table"
                    style="width: 100%"
            >
<!--                <el-table-column fixed width="50" type="selection" align="center" :reserve-selection="true" ></el-table-column>-->
                <el-table-column width="50" type="index" label="序号" align="center"></el-table-column>
                <af-table-column prop="device_name" label="设备名" align="center"></af-table-column>
                <af-table-column prop="hostname" label="主机名" align="center"></af-table-column>
                <af-table-column prop="sn" label="sn" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="install" label="install" align="center" :formatter="formatinstall"></af-table-column>
                <af-table-column prop="ip" label="ip" align="center"></af-table-column>
                <af-table-column prop="gateway" label="gateway" align="center"></af-table-column>
                <af-table-column prop="netmask" label="netmask" align="center"></af-table-column>
                <af-table-column prop="usage" label="用途" align="center"></af-table-column>
                <af-table-column prop="type" label="type" align="center"></af-table-column>
                <af-table-column prop="console_ip" label="console_ip" align="center"></af-table-column>
                <af-table-column prop="console_user" label="console_user" align="center"></af-table-column>
                <af-table-column prop="pxe_server_ip" label="pxe_server_ip" align="center"></af-table-column>
                <af-table-column prop="ipmi_server_ip" label="ipmi_server_ip" align="center"></af-table-column>
                <af-table-column prop="os_name" label="os_name" align="center"></af-table-column>
                <af-table-column prop="os_version" label="os_version" align="center"></af-table-column>
                <af-table-column prop="ks_name" label="ks_name" align="center"></af-table-column>
                <af-table-column prop="profile" label="profile" align="center"></af-table-column>
                <af-table-column prop="install_ip" label="install_ip" align="center"></af-table-column>
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
        name: "JobInstallLog",
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
                loading: true
            }
        },
        created() {
            this.getData()
        },
        methods: {
            getData(){
                this.$http.get( `automation/api/job_install/?current_page=${this.query.pageIndex}&pre_page=${
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
            //处理install 0对应成功1对应失败
            formatinstall(row) {
                return row.install == 0 ? '成功' : row.install == 1 ? '失败':" ";
            }
        }
    }
</script>

<style scoped>

</style>

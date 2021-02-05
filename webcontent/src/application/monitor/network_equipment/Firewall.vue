<template>
    <div>
        <div class="wrapper">
            <!-- <div class="crumbs">
                 <el-breadcrumb separator="/">
                     <el-breadcrumb-item>
                         <i class="el-icon-lx-cascades"></i> 防火墙
                     </el-breadcrumb-item>
                 </el-breadcrumb>
             </div>-->
            <div class="container">
                <el-form :inline="true" v-model="searchData">
                    <el-row>
                        <el-form-item>
                            <el-input v-model="searchData.ipaddr" clearable placeholder="ip" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box change_el_button" @click="handleSearch">查询</el-button>
                    </el-row>
                </el-form>
                <el-table
                        :data="tableData"
                        border
                        style="width: 100%">
                    <el-table-column prop="name" label="名称" align="center"></el-table-column>
                    <el-table-column prop="series" :formatter="serie_name_format" label="系列" align="center"></el-table-column>
                    <el-table-column prop="ipaddr" label="ip地址" align="center"></el-table-column>
                    <el-table-column prop="snmp_username" label="snmp用户名" align="center"></el-table-column>
                    <el-table-column prop="snmp_password" label="snmp密码" align="center"></el-table-column>
                    <el-table-column prop="snmp_version" label="snmp版本" align="center"></el-table-column>
                    <el-table-column prop="manufacture" label="生产厂家" align="center"></el-table-column>
                    <el-table-column prop="source" label="来源" align="center"></el-table-column>
                    <el-table-column prop="desc" label="描述" align="center"></el-table-column>
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
    </div>
</template>

<script>
    export default {
        name: "Firewall",
        data() {
            return{
                tableData: [],
                serie_name: '',
                searchData: {
                    ipaddr: "",
                    name: "",
                    type: ["FW"],
                },
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
            }
        },
        created() {
            this.getData()
        },
        methods: {
            // 格式化系列名
            serie_name_format(row) {
                if(row.series) {
                    return row.series.series_name;
                }else {
                    return ''
                }
            },
            getData() {
                this.$http.get(`asset/api/nro/network/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&ipaddr=${this.searchData.ipaddr}&name=${
                    this.searchData.name}&type=${this.searchData.type}`, {
                    headers:
                        {
                            'token': localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
            } ,
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },

        }
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/darkStyle";
</style>

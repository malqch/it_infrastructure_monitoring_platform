<template>
    <div>
        <div class="wrapper">
            <!--<div class="crumbs">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>
                        <i class="el-icon-lx-cascades"></i> 物理服务器
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div>-->
            <div class="container">
                <el-form :inline="true" v-model="searchData">
                    <el-row>
                        <el-form-item>
                            <el-input v-model="searchData.device_ip" clearable placeholder="ip" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.device_name" clearable placeholder="名称" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.hostname" clearable placeholder="主机名" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.device_status" clearable placeholder="状态" class="handle-input"></el-input>
                        </el-form-item>
                        <el-form-item>
                            <el-input v-model="searchData.maintain_status" clearable placeholder="维护状态" class="handle-input"></el-input>
                        </el-form-item>
                        <el-button icon="el-icon-search" type="primary" class="handle-box change_el_button" @click="handleSearch">查询</el-button>
                    </el-row>
                </el-form>
                <el-table
                        :data="tableData"
                        border
                        style="width: 100%">
                    <el-table-column prop="device_ip" label="ip" align="center"></el-table-column>
                    <el-table-column prop="device_name" label="名称" align="center"></el-table-column>
                    <el-table-column prop="device_status" label="状态" align="center"></el-table-column>
                    <el-table-column prop="hostname" label="主机名" align="center"></el-table-column>
                    <el-table-column prop="belong_business" label="所属业务" align="center" :formatter="querybusinessData"></el-table-column>
                    <el-table-column prop="label" label="标签" align="center" :formatter="querylabelData"></el-table-column>
                    <el-table-column prop="maintain_status" label="维护状态" align="center"></el-table-column>
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
        name: "Server",
        data() {
            return{
                tableData: [],
                searchData: {
                    device_ip: "",
                    device_name: "",
                    hostname: "",
                    device_status: "",
                    maintain_status: "",
                    device_type: "",
                    device_vendor: ""
                },
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                businessData: []
            }
        },
        created() {
            this.getData()
        },
        methods: {
            getData() {
                    this.$http.get(`asset/api/device/?current_page=${this.query.pageIndex}&pre_page=${
                        this.query.pageSize}&device_ip=${this.searchData.device_ip}&device_name=${
                        this.searchData.device_name}&device_status=${this.searchData.device_status}&device_vendor=${
                        this.searchData.device_vendor}&device_type=服务器&maintain_status=${this.searchData.maintain_status
                    }&hostname=${this.searchData.hostname}`, {
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
            //处理维护状态
            formatMarintain(row) {
                return row.maintain_status == '维护中' ? '是' : row.maintain_status == '未维护' ? '否':"";
            },
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            querybusinessData(row) {
                if(row.belong_business!=""){
                        var belong_business = ''
                        for (var v of row.belong_business) {//遍历json数组时，这么写p为索引，0,1
                            belong_business += ' ' + v.name
                        }
                        return belong_business;
                    }else{
                    return ''
                }
            },
            querylabelData(row) {
                if(row.label!=""){
                    var label = ''
                    for (var v of row.label) {//遍历json数组时，这么写p为索引，0,1
                        label += ' ' + v.tag_name
                    }
                    return label;
                }else{
                    return ''
                }
            }
        }
    }
</script>
<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    @import "../../../assets/scss/darkStyle.scss";
</style>
<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-row>
            <el-input
                    type="text"
                    placeholder="请输入脚本名"
                    v-model="keywords"
                    style="width:200px; margin-bottom:15px;"
                    clearable>
            </el-input>
<!--            <el-date-picker v-model="searchData.start_time" type="datetime" placeholder="起始日期" class="mr10">-->
<!--            </el-date-picker>-->
<!--            <el-date-picker v-model="searchData.end_time" type="datetime" placeholder="结束日期" class="mr10">-->
<!--            </el-date-picker>-->
            <el-button style="margin-left:10px;" type="primary" @click="handleSearch">查询</el-button>
            </el-row>
            <button type="button" style="background: #a6baf3" class="btn btn-primary" v-on:click="getPdf('#pdfDom')">导出巡检报告</button>
            <div class="row" id="pdfDom">
                <el-table
                        :data="tableData"
                        border
                        style="width: 100%; height: 100%"
                        max-height="600"
                >
                    <el-table-column type="selection" align="center"></el-table-column>
                    <el-table-column prop="patrol_name" label="巡检任务" align="center"></el-table-column>
                    <el-table-column prop="script_name" label="脚本名字" align="center"></el-table-column>
                    <el-table-column prop="network_ip" label="主机ip" align="center"></el-table-column>
                    <el-table-column prop="hostname" label="主机名" align="center"></el-table-column>
                    <af-table-column label="脚本输出" align="center">
                        <template slot-scope="scope_output">
                            <el-tooltip class="item" effect="dark" :content=scope_output.row.script_output placement="top-start">
                                <span>{{ scope_output.row.script_output }}</span>
                            </el-tooltip>
                        </template>
                    </af-table-column>
                    <af-table-column prop="execute_time" label="执行时间" :formatter="datetimeFormat" align="center"></af-table-column>
                    <af-table-column type="text" label="执行结果" align="center">
                        <template slot-scope="scope_res">
                            <el-tooltip class="item" effect="dark" :content=scope_res.row.execute_res placement="top-start">
                                <span>{{ scope_res.row.execute_res }}</span>
                            </el-tooltip>
                        </template>
                    </af-table-column>
                    <el-table-column prop="executor" label="执行人" align="center"></el-table-column>
                </el-table>
            </div>
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
    import { datetimeFormat } from '../../../util/formatData'
    export default {
        data() {
            return {
                options: [],
                keywords: '',
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                htmlTitle: '巡检报告',
                tableData: [],
                pageDataHtml: '',
                searchData: {
                    'start_time': '',
                    'end_time': ''
                },
                multipleSelection: [],
                delList: [],
                title: '',
                editVisible: false,
                deleteVisible: false,
                datetimeFormat: null,
                pageTotal: 0,
                form: {},
                idx: -1,
                id: -1,
            };

        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getData();
            this.datetimeFormat = datetimeFormat;
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword=this.keywords;
                let url=this.url;
                if(keyword) {
                    url=`automation/api/script_log/?name=${keyword}&current_page=${this.query.pageIndex}&pre_page=${
                        this.query.pageSize}&log_use=1`
                }else {
                    url=`automation/api/script_log/?current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}
                    &log_use=1`
                }
                this.$http.get(url, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },

            // 生成巡检报告
            generate_report() {
                this.$http.post(`automation/api/patrol/generate_report/`,
                    {'start_time': this.searchData.start_time, 'end_time': this.searchData.end_time},
                    {
                        headers:{
                            'token': this.token,
                            'username': this.username
                        }
                    }).then((res)=> {
                    this.$message.success(789);
                })
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            delAllSelection() {
                const length = this.multipleSelection.length;
                let str = '';
                this.delList = this.delList.concat(this.multipleSelection);
                for (let i = 0; i < length; i++) {
                    str += this.multipleSelection[i].name + ' ';
                }
                this.$message.error(`删除了${str}`);
                this.multipleSelection = [];
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
        },
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .tag_margin{
        margin:5px 5px 0 0;
    }
    .handle-box {
        margin-bottom: 20px;
    }
    .handle-select {
        width: 120px;
    }
    .handle-input {
        width: 300px;
        display: inline-block;
    }
    .table {
        width: 100%;
        font-size: 14px;
    }
    .red {
        color: #ff0000;
    }
    .mr10 {
        margin-right: 10px;
    }
    .table-td-thumb {
        display: block;
        margin: auto;
        width: 40px;
        height: 40px;
    }
</style>

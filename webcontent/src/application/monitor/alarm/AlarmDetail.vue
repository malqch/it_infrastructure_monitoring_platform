<template>
    <div>
        <div class="wrapper">
            <div class="container">
                <div>
                    <el-select
                            v-model="searchData.alarm_ip"
                            clearable
                            filterable
                            remote
                            :remote-method="queryalarmip"
                            placeholder="告警源"
                            class="handle-input mr10"
                            :popper-append-to-body="false">
                        <el-option
                                v-for="(domain) in alarmData"
                                :key=domain.alarm_ip
                                :label=domain.alarm_ip
                                :value=domain.alarm_ip>
                        </el-option>
                    </el-select>
                    <el-select
                            v-model="searchData.alarm_level"
                            multiple
                            placeholder="告警级别"
                            class="handle-input mr10"
                            :popper-append-to-body="false">
                        <el-option
                                label="提示"
                                value="1"></el-option>
                        <el-option
                                label="报警"
                                value="2"></el-option>
                        <el-option
                                label="重要"
                                value="3"></el-option>
                        <el-option
                                label="严重"
                                value="4"></el-option>
                        <el-option
                                label="紧急"
                                value="5"></el-option>
                    </el-select>
                    <el-select
                            v-model="searchData.alarm_status"
                            clearable
                            placeholder="告警状态"
                            class="handle-input mr10"
                            :popper-append-to-body="false">
                        <el-option value="告警中"></el-option>
                        <el-option value="处理中"></el-option>
                        <el-option value="告警升级"></el-option>
                        <el-option value="已处理"></el-option>
                    </el-select>
                    <el-date-picker v-model="searchData.alarm_last_time1" type="datetime" placeholder="起始日期" class="mr10">
                    </el-date-picker>
                    <el-date-picker v-model="searchData.alarm_last_time2" type="datetime" placeholder="结束日期" class="mr10">
                    </el-date-picker>
                    <el-button icon="el-icon-search" class="handle-box change_el_button" @click="handleSearch">查询</el-button>
                </div>
                <el-table
                        :data="tableData"
                        border
                        tooltip-effect="dark"
                        style="width: 100%; cursor:pointer">
                    <el-table-column type="index" label="序号" align="center"></el-table-column>
                    <el-table-column prop="alarm_ip" label="告警源ip" align="center" width="120" ></el-table-column>
                    <el-table-column prop="alarm_strategy" label="告警策略" align="center" width="120" ></el-table-column>
                    <el-table-column
                            prop="alarm_level"
                            label="告警级别"
                            sortable
                            align="center">
                        <div slot-scope="scope" style="font-size: 10px">
                            <span v-if="scope.row.alarm_level=='5'">
                                <img :src="imgUrl2" style="width: 30px">
                                {{ '紧急' }}
                            </span>
                            <span v-else-if="scope.row.alarm_level=='4'">
                        <img :src="imgUrl4" style="width: 30px">
                        {{ '严重' }}</span>
                            <span v-else-if="scope.row.alarm_level=='3'">
                        <img :src="imgUrl5" style="width: 30px">
                        {{ '重要' }}</span>
                            <span v-else-if="scope.row.alarm_level=='2'">
                        <img :src="imgUrl3" style="width: 30px">
                        {{ '报警' }}</span>
                            <span v-else-if="scope.row.alarm_level=='1'">
                        <img :src="imgUrl1" style="width: 30px">
                        {{ '提示' }}
                    </span>
                        </div>
                    </el-table-column>
                    <el-table-column prop="alarm_status" label="告警状态" align="center" sortable>
                        <div slot-scope="scope" style="font-size: 10px">
                            <span v-if="scope.row.alarm_status=='已处理'" style="color: #16d924">
                            {{scope.row.alarm_status}}</span>
                            <span v-else-if="scope.row.alarm_status=='处理中'" style="color: #869dff">
                            {{scope.row.alarm_status}}</span>
                            <span v-else-if="scope.row.alarm_status=='告警中'" style="color: #e6360e">
                            {{scope.row.alarm_status}}</span>
                            <span v-else-if="scope.row.alarm_status=='告警升级'" style="color: #fff80f">
                            {{scope.row.alarm_status}}</span>
                        </div>
                    </el-table-column>
                    <el-table-column prop="indicator_name" label="监控指标" align="center" width="120"></el-table-column>
<!--                    <el-table-column prop="notice_code" label="通知方式" align="center" sortable>-->
<!--                        <template scope="scope" style="font-size: 10px">-->
<!--                        <span v-if="scope.row.notice_code=='1'">-->
<!--                            {{"邮件"}}-->
<!--                        </span>-->
<!--                            <span v-else-if="scope.row.notice_code=='2'">-->
<!--                            {{"短信"}}-->
<!--                        </span>-->
<!--                            <span v-else-if="scope.row.notice_code=='3'">-->
<!--                            {{"电话"}}-->
<!--                        </span>-->
<!--                        </template>-->
<!--                    </el-table-column>-->
                    <el-table-column prop="server_type" label="告警类型" align="center" sortable width="110"></el-table-column>
                    <el-table-column prop="alarm_count" label="告警数量" align="center" sortable></el-table-column>
                    <el-table-column prop="alarm_last_time" :formatter="dateFormat" sortable label="最新告警时间" align="center" width="140"></el-table-column>
                    <el-table-column prop="alarm_first_time" :formatter="dateFormat" sortable label="第一次告警时间" align="center" width="140"></el-table-column>
                    <el-table-column prop="alarm_time" :formatter="dateFormat" sortable label="接警时间" align="center" width="140"></el-table-column>
                    <el-table-column prop="finish_time" :formatter="dateFormat" sortable label="完成时间" align="center" width="140"></el-table-column>
                    <el-table-column label="操作"  align="center" width="150">
                        <div slot-scope="scope">
                            <el-button
                                    type="text"
                                    :disabled="scope.row.disable1"
                                    @click="handleEdit(scope.row,1)"
                            >接警
                            </el-button>
                            <el-button
                                    type="text"
                                    :disabled="scope.row.disable2"
                                    @click="handleEdit(scope.row,2)"
                            >升级
                            </el-button>
                            <el-button
                                    type="text"
                                    :disabled="scope.row.disable3"
                                    class="handle-box-1"
                                    @click="handleEdit(scope.row,3)"
                            >完成
                            </el-button>
                        </div>
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
        </div>
    </div>
</template>


<script>
    export default {
        name: "alarmDetail",
        data() {
            return {
                imgUrl1: '',
                imgUrl2: '',
                imgUrl3: '',
                imgUrl4: '',
                imgUrl5: '',
                searchData: {
                    alarm_ip: '',
                    alarm_level: '',
                    alarm_status: '',
                    indicator_name: '',
                    server_type:'',
                    alarm_last_time1:'',
                    alarm_last_time2:''
                },
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                alarmData: [],
                alarmDetail: [{}],
                alarmVisible: false,
                multipleSelection: [],
                // 用于存放被选中行的index
                numbers: [],
                delList: [],
                pageTotal: 0,
                form:{},
                idx: -1,
                id: -1,
                name: ''
            };
        },
        created() {
            //页面刚进入时开启长连接
            this.getData();
            // this.initWebSocket();
            let urlTemp1 = "assets/remind.png";
            let urlTemp2 = "assets/fire.png";
            let urlTemp3 = "assets/attention.png";
            let urlTemp4 = "assets/serious.png";
            let urlTemp5 = "assets/import.png";
            this.imgUrl1 = require("@/"+urlTemp1)
            this.imgUrl2 = require("@/"+urlTemp2)
            this.imgUrl3 = require("@/"+urlTemp3)
            this.imgUrl4 = require("@/"+urlTemp4)
            this.imgUrl5 = require("@/"+urlTemp5)

        },
        mounted() {
        },
        beforeDestroy() {
        },
        methods: {
            /*checkDel: function({row, rowIndex}) {
                    row.index = rowIndex;
                    if (this.tableData[rowIndex].alarm_level == 1) {
                        return 'green_icon'
                    } else if (this.tableData[rowIndex].alarm_level == 2) {
                        return 'blue'
                    } else if (this.tableData[rowIndex].alarm_level == 3) {
                        return 'yellow'
                    } else if (this.tableData[rowIndex].alarm_level == 4) {
                        return 'orange'
                    } else if (this.tableData[rowIndex].alarm_level == 5) {
                        return 'red'
                    }
                },*/

            // 获取 easy-mock 的模拟数据
            getData() {
                if (this.searchData.alarm_last_time1) {
                    this.searchData.alarm_last_time1 = this.timeD(this.searchData.alarm_last_time1)
                }
                if (this.searchData.alarm_last_time2) {
                    this.searchData.alarm_last_time2 = this.timeD(this.searchData.alarm_last_time2)
                }
                this.$http.get(`monitor/api/alarm_detail/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&alarm_ip=${this.searchData.alarm_ip}&alarm_level=${
                    this.searchData.alarm_level}&alarm_last_time1=${this.searchData.alarm_last_time1}&alarm_last_time2=${
                    this.searchData.alarm_last_time2}&alarm_status=${this.searchData.alarm_status}&indicator_name=${
                    this.searchData.indicator_name}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    for (let i in this.tableData) {
                        this.$set(this.tableData[i], 'disable1', false)
                        this.$set(this.tableData[i], 'disable2', false)
                        this.$set(this.tableData[i], 'disable3', false)
                        if (this.tableData[i].alarm_status === '处理中') {
                            this.tableData[i].disable1 = true
                        } else if (this.tableData[i].alarm_status === '告警升级') {
                            this.tableData[i].disable2 = true
                        } else if (this.tableData[i].alarm_status === '已处理') {
                            this.tableData[i].disable1 = true
                            this.tableData[i].disable2 = true
                            this.tableData[i].disable3 = true
                        }
                        if (this.tableData[i].alarm_strategy == '1') {
                            this.tableData[i].alarm_strategy = '轮询次数'
                        } else if (this.tableData[i].alarm_strategy == '2') {
                            this.tableData[i].alarm_strategy = '轮询平均值'
                        } else if (this.tableData[i].alarm_strategy == '3') {
                            this.tableData[i].alarm_strategy = '持续时间'
                        } else {
                            this.tableData[i].alarm_strategy = '平均时间'
                        }
                    }
                    this.pageTotal = res.data.total_count;
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                },
            queryalarmip (query) {
                this.$http.get(`monitor/api/alarm_detail/alarm/?query=${query}`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.alarmData = res.data
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            handleEdit(row,num) {
                if (num === 1) {
                    row.alarm_status = '处理中'
                    row.disable1 = true
                } else if (num === 2) {
                    row.alarm_status = '告警升级'
                    row.disable2 = true
                } else if (num === 3) {
                    console.log(row,123)
                    row.alarm_status = '已处理'
                    row.disable1 = true
                    row.disable2 = true
                    row.disable3 = true
                }
                this.$http.put(`monitor/api/alarm_detail/status/`,
                    {
                        'id': row.id,
                        'alarm_status': row.alarm_status
                    },
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    if (res.status === 200) {
                        this.$message.success('操作成功！');
                        this.editVisible = false;
                        row.disable = true;
                        this.getData()
                    }
                }).catch((error) => {
                    this.$message.error('邮件发送失败！');
                    console.log(JSON.stringify(error.response.data));
                });
            },
            /*getAlarmDetail(row) {
                this.id = row.id;
                console.log(row);
                this.alarmDetail.push(row)
                this.alarmVisible = true
            },*/
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
            timeD (time) {
                let d = new Date(time);
                const year = d.getFullYear();
                const month = d.getMonth() + 1;
                const day = d.getDate();
                const hh = d.getHours();
                const mm = d.getMinutes();
                const ss = d.getSeconds();
                const timeFormat = year + "-" + month + "-" + day + " " + hh + ":" + mm + ":" + ss;
                console.log(timeFormat)
                return timeFormat
            },
           /* timeP(s) {
                return s<10?'0'+s:s
                }*/
        }
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/darkStyle.scss";
    .handle-box {
        margin-bottom: 20px;
    }
    .handle-input {
        width: 150px;
        display: inline-block;
    }
	/deep/ .el-menu{
	    background-color: #494b79;
	}
</style>

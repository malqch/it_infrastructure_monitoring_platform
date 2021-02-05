<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-col :span="24" :inline="true">
                <el-input
                        type="text"
                        placeholder="请输入脚本名"
                        v-model="keywordsName"
                        style="width:200px; margin-bottom:15px;"
                        clearable>
                </el-input>
                <el-select style="width:200px; margin-left:10px;" clearable v-model="keywordsStatus" placeholder="请选择脚本状态"
                >
                    <el-option
                            v-for="item in typeOptions"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
                <el-button style="margin-left:10px;" type="primary" @click="handleSearch">查询</el-button>
            </el-col>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="script_name" label="脚本名字" align="center"></el-table-column>
<!--                <el-table-column prop="host_info" label="host_info" align="center"></el-table-column>-->
                <el-table-column prop="host_info" label="host_info" align="center">
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchHostLabel(scope.row)" class="color-link">查看主机信息</el-link>
                    </template>
                </el-table-column>
                <el-table-column prop="execute_type" label="执行方式" align="center"></el-table-column>
                <el-table-column label="执行时间" align="center">
                    <template slot-scope="scope_time">
                        <el-tooltip class="item" effect="dark" :content=scope_time.row.execute_time placement="top-start">
                            <span>{{ scope_time.row.execute_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column prop="execute_week" label="每周几执行" align="center"></el-table-column>
                <el-table-column label="开始时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_start_time">
                        <el-tooltip class="item" effect="dark" :content=scope_start_time.row.start_time placement="top-start">
                            <span>{{ scope_start_time.row.start_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column label="结束时间" :formatter="datetimeFormat" align="center">
                    <template slot-scope="scope_end_time">
                        <el-tooltip class="item" effect="dark" :content=scope_end_time.row.end_time placement="top-start">
                            <span>{{ scope_end_time.row.end_time }}</span>
                        </el-tooltip>
                    </template>
                </el-table-column>
                <el-table-column prop="status" :formatter="scriptStatus" label="状态" align="center"></el-table-column>
                <el-table-column prop="executor" label="执行人" align="center"></el-table-column>
                <el-table-column prop="uuid" label="唯一标识符" align="center"></el-table-column>
                <el-table-column prop="create_time" label="创建时间" align="center"></el-table-column>
                <el-table-column label="操作" align="center" width="150px">
                    <template slot-scope="scope">
                        <el-button
                                v-if="scope.row.execute_type ==='定时执行'"
                                type="text"
                                icon="el-icon-video-pause"
                                disabled
                                @click="handlePause(scope.$index, scope.row)"
                        >暂停</el-button>
                        <el-button
                                v-if="scope.row.execute_type !=='定时执行' && scope.row.status === 0"
                                type="text"
                                icon="el-icon-video-pause"
                                class="color-link"
                                @click="handlePause(scope.$index, scope.row)"
                        >暂停</el-button>
                        <el-button
                                v-if="scope.row.execute_type !=='定时执行' && scope.row.status === 1"
                                type="text"
                                icon="el-icon-video-play"
                                class="color-green"
                                @click="handleResume(scope.$index, scope.row)"
                        >重启</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
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
        <!-- 添加主机弹出框 -->
        <el-dialog title="主机信息" :visible.sync="hostLabelVisible" width="35%" class="alert_dialog">
            <ul :model="hostLabelData[0]" v-for="item in hostLabelData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">network_ip:</label>
                    <span class="network_span">{{item.network_ip}}</span>
                    <label class="network_label">hostname:</label>
                    <span class="network_span">{{item.hostname}}</span>
                    <label class="network_label">type:</label>
                    <span class="network_span">{{item.type}}</span>
                </li>
            </ul>
        </el-dialog>
        <!-- 暂停弹出框 -->
        <el-dialog title="提示" :visible.sync="pauseVisible" width="25%">
            <span>确定暂停定时任务 {{uuid}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="pauseVisible = false">取 消</el-button>
                <el-button type="primary" @click="pauseTimedTask">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 重启弹出框 -->
        <el-dialog title="提示" :visible.sync="resumeVisible" width="25%">
            <span>确定重启定时任务 {{uuid}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="resumeVisible = false">取 消</el-button>
                <el-button type="primary" @click="resumeTimedTask">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除定时任务 {{uuid}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteTimedTask">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    import { datetimeFormat } from '../../../util/formatData'
    import { getFormatDate } from '../../../util/formatData'
    export default {
        data() {
            return {
                options: [],
                keywordsName: '',
                keywordsStatus: '',
                typeOptions: [
                    {
                        value: '1',
                        label: '已暂停'
                    }, {
                        value: '0',
                        label: '运行中'
                    }
                ],
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                title: '',
                uuid: '',
                editVisible: false,
                deleteVisible: false,
                pauseVisible: false,
                resumeVisible: false,
                hostLabelVisible: false,
                hostLabelData: [],
                pageTotal: 0,
                form: {},
                datetimeFormat: null,
                loading: true,
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
                this.$http.get(`automation/api/script_timed_task/?name=${this.keywordsName}&status=${this.keywordsStatus}&current_page=${this.query.pageIndex}&pre_page=${this.query.pageSize}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                    this.loading = false;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
                });
            },
            //查看主机信息
            searchHostLabel(row) {
                this.hostLabelData = JSON.parse(row.host_info);
                this.hostLabelVisible = true;
            },
            scriptStatus(row) {
                if (row.status === 0) {
                    return '运行中'
                } else {
                    return '已暂停'
                }
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 触发暂停按钮
            handlePause(index, row) {
                this.uuid = row.uuid;
                this.pauseVisible = true;
            },
            // 暂停定时任务
            pauseTimedTask() {
                this.$http.post(`automation/api/script/pause_timed_task/`,
                    {'uuid': this.uuid},
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('暂停成功！');
                        this.pauseVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('暂停失败！');
                        this.pauseVisible = false;
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.pauseVisible = false;
                });
            },
            // 触发重启按钮
            handleResume(index, row) {
                var exec_end_time = this.execEndDatetimeFormat(row.end_time);
                var now_time = this.execEndDatetimeFormat(getFormatDate());
                if(row.end_time && exec_end_time<now_time) {
                    this.$message.warning('重启失败，结束时间小于当前时间，请重新选择！');
                }else {
                    this.uuid = row.uuid;
                    this.resumeVisible = true;
                }
            },
            // 格式化结束时间
            execEndDatetimeFormat(end_time){
                if(end_time!=null){
                    const dateMat = new Date(end_time);
                    return dateMat.getTime();
                }
            },
            // 重启定时任务
            resumeTimedTask() {
                this.$http.post(`automation/api/script/restart_timed_task/`,
                    {'uuid': this.uuid},
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('重启成功！');
                        this.resumeVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('重启失败！');
                        this.resumeVisible = false;
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.resumeVisible = false;
                });
            },
            // 触发删除按钮
            handleDelete(index, row) {
                this.uuid = row.uuid;
                this.deleteVisible = true;
            },
            // 删除定时任务
            deleteTimedTask() {
                this.$http.post(`automation/api/script/remove_timed_task/`,
                    {'uuid': this.uuid},
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                    if(res.status === 200) {
                        this.$message.success('删除成功！');
                        this.deleteVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('删除失败！');
                        this.deleteVisible = false;
                    }
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.deleteVisible = false;
                });
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
    .color-green{
        color: #2ccc0a;
    }
</style>

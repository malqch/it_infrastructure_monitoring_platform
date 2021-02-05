<template slot-scope="scope">
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" ref="form" :model="form" :rules="rules" label-width="100px">
                <el-row type="flex" class="row-bg">
                    <el-form-item label="巡检任务:" prop="patrol">
                        <el-select v-model="form.patrol" @focus="getPatrol" placeholder="请选择巡检任务" clearable>
                            <el-option v-for="item in patrolData"
                                    :key=item.id
                                    :label=item.patrol_name
                                    :value="`${item.start_time}/${item.end_time}/${item.script[0]}/${item.id}`">
                            </el-option>
                        </el-select>
                    </el-form-item>
                </el-row>
                <el-row :span="15">
                    <el-form-item label="汇总:" prop="param" labelWidth="120">
                        已选 <label class="blue">{{rowLength}}</label> 台
                    </el-form-item>
                </el-row>
                <el-row :span="9">
                    <el-button class="el-icon-circle-plus-outline" type="primary" plain  @click="handleAddHost">添加主机</el-button>
                    <el-button class="el-icon-caret-right" type="success" plain @click="handleExecScript" :disabled=disabled>执行</el-button>
                </el-row>
            </el-form>
            <el-table
                    :data="tableDataSelect"
                    border
                    style="width: 100%"
                    max-height="600"
            >
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="hostname" label="主机名称" align="center"></el-table-column>
                <el-table-column prop="network_ip" label="内网IP" align="center"></el-table-column>
                <el-table-column prop="type" label="类型" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" align="center"></el-table-column>
                <el-table-column prop="password" label="密码" align="center"></el-table-column>
                <el-table-column label="操作" align="center">
                    <template slot-scope="scope">
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDelete(scope.$index, scope.row)"
                        >删除</el-button>
                    </template>
                </el-table-column>
            </el-table>
        </div>
        <!-- 添加主机弹出框 -->
        <el-dialog title="添加主机" :visible.sync="addHostVisible" width="70%">
            <el-form :inline="true" ref="host_form" :model="host_form" label-width="100px">
                <el-form-item label="选择主机:" prop="room_type">
                    <el-select v-model="host_form.room_type" placeholder="机房分类" clearable>
                        <el-option
                                v-for="item in room_type_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-input
                            type="text"
                            placeholder="请输入主机名"
                            v-model="keywords"
                            style="width:200px; margin-bottom:15px;"
                            clearable>
                    </el-input>
                </el-form-item>
                <el-button @click="handleSearch">查询</el-button>
            </el-form>
            <el-table
                    :data="tableData"
                    border
                    style="width:100%"
                    max-height="600"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" align="center" :selectable="selectable"></el-table-column>
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="hostname" label="主机名称" align="center"></el-table-column>
                <el-table-column label="内网IP" align="center">
                    <template slot-scope="host_scope">
                        <el-select v-model="host_scope.row.network_ip"  @focus="getNetworkIp(host_scope.row)" placeholder="请选择内网ip">
                            <el-option
                                    v-for="item in network_ip_option"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                            </el-option>
                        </el-select>
                    </template>
                </el-table-column>
                <el-table-column prop="type" label="类型" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" align="center"></el-table-column>
                <el-table-column prop="password" label="密码" align="center"></el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHostVisible = false">取 消</el-button>
                <el-button type="primary" @click="addHost">添 加</el-button>
            </span>
        </el-dialog>

        <!-- 选择脚本时间弹出框 -->
        <el-dialog title="执行方式" :visible.sync="CrontabVisible" width="55%">
            <el-form ref="form" :rules="rules" :model="form" label-width="120px">
                <el-form-item label="选择执行方式：" prop="exec_type">
                    <el-select v-model="form.exec_type" style="width:320px;" placeholder="请选择任务执行方式">
                        <el-option
                                v-for="item in exec_type_options"
                                :key="item.value"
                                :label="item.label"
                                :value="item.label">
                        </el-option>
                    </el-select>
                </el-form-item>
<!--                <el-form-item v-if="form.exec_type !== '定时执行'" label="选择开始时间：" prop="start_time">-->
<!--                    <el-date-picker-->
<!--                            v-model="form.start_time"-->
<!--                            type="datetime"-->
<!--                            disabled="false"-->
<!--                            style="width:320px;"-->
<!--                            placeholder="请选择任务开始时间"-->
<!--                            value-format="yyyy-MM-dd HH:mm:ss">-->
<!--                    </el-date-picker>-->
<!--                </el-form-item>-->
<!--                <el-form-item v-if="form.exec_type !== '定时执行'" label="选择结束时间：" prop="end_time">-->
<!--                    <el-date-picker-->
<!--                            v-model="form.end_time"-->
<!--                            type="datetime"-->
<!--                            disabled="false"-->
<!--                            style="width:320px;"-->
<!--                            placeholder="请选择任务结束时间"-->
<!--                            value-format="yyyy-MM-dd HH:mm:ss">-->
<!--                    </el-date-picker>-->
<!--                </el-form-item>-->
<!--                <el-form-item v-if="form.exec_type === '定时执行'" label="选择执行时间：" prop="exec_time">-->
<!--                    <el-date-picker-->
<!--                            v-model="form.exec_time"-->
<!--                            type="datetime"-->
<!--                            style="width:320px;"-->
<!--                            placeholder="请选择任务执行时间"-->
<!--                            value-format="yyyy-MM-dd HH:mm:ss">-->
<!--                    </el-date-picker>-->
<!--                </el-form-item>-->
                <el-form-item v-if="form.exec_type === '周期性执行'" label="输入执行时间：" prop="cron_exec_time">
                    <el-input v-model="form.cron_exec_time" @blur="checkDate" style="width:320px;" placeholder="请输入执行时间"></el-input>
                    <el-row class="cron_time_color">格式:分 时 日 月 年,以空格间隔</el-row>
                    <el-row class="cron_exec_time">
                        <el-col>周期性执行执行时间采用Cron表达式:</el-col>
                        <ul>
                            <li>逗号（“ , “）分开的值，例如：“1,3,4,7,8”</li>
                            <li>连词符（“ - “）指定值的范围，例如：“1-6”，意思等同于“1,2,3,4,5,6”</li>
                            <li>星号（“ * “）代表任何可能的值。例如，在“小时域”里的星号等于是“每一个小时”</li>
                            <li>斜线（“ / “）操作符，用于表示跳过某些给定的数。例如，“*/3”在小时域中等于“0,3,6,9,12,15,18,21”等被3整除的数</li>
                        </ul>
                    </el-row>
                </el-form-item>
<!--                <el-form-item v-if="form.exec_type === '周期性执行'" label="每周几执行：" prop="exec_week">-->
<!--                    <el-input v-model="form.exec_week" disabled style="width:320px;" placeholder="星期（0-6 或者 mon，tue，wed，thu，fri，sat，sun）"></el-input>-->
<!--                    &lt;!&ndash;                    <el-col class="line" :span="-1">-</el-col>&ndash;&gt;-->
<!--                </el-form-item>-->
<!--                <el-form-item v-if="form.exec_type === '轮巡执行'" label="输入执行时间：" prop="interval_exec_time">-->
<!--                    <el-input v-model="form.interval_exec_time" @blur="checkTime" style="width:320px;" placeholder="请输入执行时间"></el-input>-->
<!--                    <el-col class="cron_time_color">格式:时/分/秒,以(/)间隔</el-col>-->
<!--                </el-form-item>-->

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="CrontabVisible = false">取 消</el-button>
                <el-button type="primary" @click="timingExecScript">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 脚本立即执行弹出框 -->
        <el-dialog title="执行" :visible.sync="immediateExecVisible" width="40%" class="row-bg" :close-on-click-modal="false">
            <el-row v-for="item in scriptMessage" :key="item">
                <el-col :span="24" style="margin-top:10px;">
                    <span>{{ item }}</span>
                </el-col>
            </el-row>
        </el-dialog>
    </div>
</template>

<script>
    import ElCol from "element-ui/packages/col/src/col";
    import { getFormatDate } from '../../../util/formatData';
    export default {
        components: {ElCol},
        name: 'roletable',
        data() {
            return {
                options: [],
                addHostVisible: false,
                CrontabVisible: false,
                ExecVisible: false,
                immediateExecVisible: false,
                network_ip_option: [],
                menuProps: {
                    value: 'id',
                    label: 'name',
                    multiple: true
                },
                keywords: '',
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                patrolData: [],
                tableDataSelect: [],
                multipleSelection: [],
                delList: [],
                disabled: true,
                title: '',
                name: '',
                startFormatDate: '',
                endFormatDate: '',
                scriptLogMessage:{
                    execute_res: ''
                },
                wsUrl: '',
                scriptMessage: [],
                pageTotal: 0,
                form: {
                },
                host_form: {},
                host: {},
                idx: -1,
                id: -1,
                room_type_options: [
                    {
                        value: '选项1',
                        label: '公司机房'
                    }, {
                        value: '选项2',
                        label: '外部机房'
                    }
                ],
                exec_type_options: [
                   {
                        value: '选项2',
                        label: '周期性执行'
                    }
                ],
                rules: {
                    patrol: [
                        { required: true, message: '请选择巡检任务', trigger: 'change' }
                    ]
                },
                rowLength:0
            };
        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword=this.keywords;
                let url=this.url;
                if(keyword) {
                    url=`asset/api/network/network_type?hostname=${keyword}`
                }else {
                    url=`asset/api/network/network_type/`
                }
                this.$http.get(url, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    res.data.map( item =>{ item['network_ip']=item['network_ip'][0] });
                    this.tableData = res.data;
                    // this.pageTotal = res.data.total_count;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 查询内网ip
            getNetworkIp(row) {
                this.$http.get(`asset/api/network/network_type?hostname=${row.hostname}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    this.network_ip_option = res.data[0]['network_ip'];
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 查询巡检任务信息
            getPatrol() {
                const status = '未执行'
                this.$http.get(`automation/api/patrol/?status=${status}`,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    console.log(res.data,111)
                    console.log(res.status,222)
                    if(res){
                        this.patrolData = res.data;
                    }
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发添加主机按钮
            handleAddHost() {
                this.addHostVisible = true;
                this.getData();
            },
            // 添加主机
            addHost() {
                if(this.tableDataSelect.length===0) {
                    this.tableDataSelect = this.multipleSelection;
                }else {
                    this.tableDataSelect = this.tableDataSelect.concat(this.multipleSelection);
                }
                this.addHostVisible = false;
                this.disabled = false;
                this.rowLength=this.tableDataSelect.length;
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 触发删除按钮
            handleDelete(index) {
                this.tableDataSelect.splice(index, 1);
                if (this.tableDataSelect.length===0) {
                    this.disabled = true;
                }
                this.rowLength=this.tableDataSelect.length;
            },
            // 多选操作
            handleSelectionChange(val) {
                this.multipleSelection = val;
            },
            genID(length){
                return Number(Math.random().toString().substr(3,length) + Date.now()).toString(36);
            },

            // 处理执行巡检任务
            handleExecScript() {
                const end_time = this.form.patrol.split('/')[1]
                if (new Date().getTime() < new Date(end_time).getTime()) {
                    this.CrontabVisible = true;
                } else {
                    this.$message.error('执行失败！巡检任务结束时间已过!');
                }

            },

            // 立即执行脚本
            execScript() {
                if(this.form.script_name) {
                    if(this.tableDataSelect.length > 1) {
                        this.$message.warning('单机执行，只能选择一台主机！');
                    }else {
                        this.form.host_info = this.tableDataSelect;
                        this.form.uuid = this.genID();
                        this.form.username = this.username;
                        this.scriptMessage = [];
                        this.immediateExecVisible = true;
                        this.wsUrl = this.globalAPI.websocketUrl + `ws/immediate_exec_script/`;
                        this.initWebSocket();
                    }}else {
                    this.$message.warning('请选择脚本名称！');
                }
            },
            // 校验执行时间格式
            checkDate() {
                const reg=/^([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)$/;
                if(reg.test(this.form.cron_exec_time)===false){
                    this.$message.warning('执行时间格式不正确！');
                    return false;
                }else {
                    return true;
                }
            },
            checkTime() {
                const reg=/^([0-1]?[0-9]|2[0-3])\/([0-5][0-9])\/([0-5][0-9])$/;
                if(reg.test(this.form.interval_exec_time)===false){
                    this.$message.warning('执行时间格式不正确！');
                    return false;
                }else {
                    return true;
                }
            },
            // 定时执行脚本
            timingExecScript() {
                if(this.form.exec_type === '周期性执行') {
                    if (this.checkDate()===false) {
                        return;
                    }
                }else if(this.form.exec_type === '周期性执行') {
                    if (this.checkTime()===false) {
                        return;
                    }
                }
                this.form.host_info = this.tableDataSelect;
                this.form.uuid = this.genID();
                console.log(this.form.patrol,123)
                this.form.patrol = this.form.patrol.split('/')
                console.log(this.form.patrol,234)
                this.form.start_time = this.form.patrol[0];
                this.form.end_time = this.form.patrol[1];
                this.form.patrol_id = this.form.patrol[3]
                const script_id = this.form.patrol[2];
                console.log(script_id,999)
                this.$http.get(`automation/api/script/?id=${script_id}`,
                    {
                        headers:{
                            'token': this.token
                        }
                    }).then((res)=>{
                        const scriptData = res.data[0];
                        this.form.id = scriptData.id;
                        this.form.script_name = scriptData.script_name;
                        this.form.script_type = scriptData.script_type;
                        this.form.category = scriptData.category;
                        this.form.content = scriptData.content;
                        this.form.desc = scriptData.desc;
                        this.form.use = scriptData.use;
                        this.form.param = scriptData.param;
                        this.form.test_status = scriptData.test_status;
                        this.form.ef_time = scriptData.ef_time;
                        console.log(this.form, 888)
                        this.$refs.form.validate((valid) => {
                            if (valid) {
                                this.$http.post(`automation/api/script/timing_exec_script/`,
                                    this.form,
                                    {
                                        headers:{
                                            'token': this.token,
                                            'username': this.username
                                        }
                                    }).then((res)=>{
                                    console.log(123456)
                                    this.CrontabVisible = false;
                                    this.$message.success(res.data.msg);
                                    // this.$router.push('/automation/script_log');
                                }).catch(  (error) => {
                                    this.$message.error(JSON.stringify(error.response.data));
                                });
                            } else {
                                this.$message.warning('请选择必填项');
                                return false;
                            }
                        });
                }).catch((error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                })
            },


            // 删除全选
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
            selectable(row){
                if(this.tableDataSelect.some( ele => {return ele.hostname===row.hostname})){
                    return false;
                }else{
                    return true;
                }
            }
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
    .blue{
        color: #409eff;
    }
    .row-bg /deep/ .el-form-item__content{
        width: 166px;
    }
    .row-bg /deep/ .el-dialog__title,.row-bg /deep/ .el-dialog__body{
        color:#fff;
    }
    .center{
        text-align: center;
    }
    .cron_exec_time{
        background: #f4f5f5;
        border: 1px solid #EBEEF5;
        padding: 14px;
        font-size:12px;
        ul{
            margin-left:12px;
        }
    }
    .cron_time_color{
        color:#919191;
    }
    .row-bg /deep/ .el-dialog__body{
        background-color: #0f0f0f;
    }
    .row-bg /deep/ .el-dialog__header{
        background-color: #1e1e1e;
    }
</style>

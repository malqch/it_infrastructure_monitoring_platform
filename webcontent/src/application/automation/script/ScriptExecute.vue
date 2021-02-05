<template slot-scope="scope">
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" ref="form" :model="form" :rules="rules" label-width="100px">
                <el-row type="flex" class="row-bg">
                    <el-form-item label="所属分类:" prop="category">
                        <el-select v-model="form.category" @change="selectScriptByCategory" placeholder="请选择脚本所属分类">
                            <el-option
                                    v-for="item in script_category_options"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="脚本类型:" prop="script_type">
                        <el-select v-model="form.script_type" @change="selectScriptByScriptType" placeholder="请选择脚本类型">
                            <el-option
                                    v-for="item in script_type_options"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="脚本名称:" prop="script_name">
                        <el-select v-model="form.script_name" @change="selectScriptByScriptName" placeholder="请选择脚本">
                            <el-option
                                    v-for="item in script_name_options"
                                    :key="item"
                                    :label="item"
                                    :value="item">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-form-item label="测试状态:" prop="test_status">
                        <el-input v-model="form.test_status" clearable></el-input>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-form-item label="脚本说明:" prop="desc">
                        <el-input type="textarea" :cols="140" v-model="form.desc" placeholder="脚本描述"></el-input>
                    </el-form-item>
                </el-row>
                <el-row>
                    <el-form-item label="脚本参数:" prop="param">
                        <el-input type="textarea" v-model="form.param" :cols="140" placeholder="多个参数必须以空格间隔"></el-input>
                    </el-form-item>
                </el-row>
                <div type="flex" class="row-bg" justify="space-around">
                    <el-col :span="15">
                        <el-form-item label="汇总:" prop="param" labelWidth="120">
                            已选 <label class="blue">{{rowLength}}</label> 台
                        </el-form-item>
                    </el-col>
                    <el-col :span="9">
                        <el-button class="el-icon-circle-plus-outline" type="primary" plain  @click="handleAddHost">添加主机</el-button>
                        <el-button class="el-icon-caret-right" type="success" plain @click="immediateExecScript" :disabled=disabled>单机执行</el-button>
                        <el-button class="el-icon-s-unfold" type="info" plain @click="batchExecScript" :disabled=disabled>批量执行</el-button>
                        <el-button class="el-icon-time" type="warning" plain @click="handleCrontab" :disabled="disabled">定时执行</el-button>
                    </el-col>
                </div>
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
                <el-table-column prop="password" label="密码" :formatter="formatPwd" align="center"></el-table-column>
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
                <el-button type="primary" @click="handleSearch">查询</el-button>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width:100%"
                    max-height="600"
                    @selection-change="handleSelectionChange"
            >
                <el-table-column type="selection" align="center" :selectable="selectable"></el-table-column>
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="hostname" label="主机名称" align="center"></el-table-column>
                <el-table-column prop="network_ip" label="内网IP" align="center">
<!--                    <template slot-scope="host_scope">-->
<!--                        <el-select v-model="host_scope.row.network_ip"  @focus="getNetworkIp(host_scope.row)" placeholder="请选择内网ip">-->
<!--                            <el-option-->
<!--                                    v-for="item in network_ip_option"-->
<!--                                    :key="item"-->
<!--                                    :label="item"-->
<!--                                    :value="item">-->
<!--                            </el-option>-->
<!--                        </el-select>-->
<!--                    </template>-->
                </el-table-column>
                <el-table-column prop="operate_system" label="系统类型" align="center"></el-table-column>
                <el-table-column prop="type" label="类型" align="center"></el-table-column>
                <el-table-column prop="username" label="用户名" align="center"></el-table-column>
                <el-table-column prop="password" label="密码" :formatter="formatPwd" align="center"></el-table-column>
                <el-table-column prop="ssh_port" label="端口" align="center"></el-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHostVisible = false">取 消</el-button>
                <el-button type="primary" @click="addHost">添 加</el-button>
            </span>
        </el-dialog>
        <!-- 定时任务弹出框 -->
        <el-dialog title="定时任务" :visible.sync="CrontabVisible" width="55%">
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
                <el-form-item v-if="form.exec_type === '定时执行'" label="选择执行时间：" prop="exec_time">
                    <el-date-picker
                            v-model="form.exec_time"
                            type="datetime"
                            style="width:320px;"
                            placeholder="请选择任务执行时间"
                            value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                </el-form-item>
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
                <el-form-item v-if="form.exec_type === '周期性执行'" label="每周几执行：" prop="exec_week">
                    <el-input v-model="form.exec_week" style="width:320px;" placeholder="星期（0-6 或者 mon，tue，wed，thu，fri，sat，sun）"></el-input>
                    <!--                    <el-col class="line" :span="-1">-</el-col>-->
                </el-form-item>
                <el-form-item v-if="form.exec_type === '轮巡执行'" label="输入执行时间：" prop="interval_exec_time">
                    <el-input v-model="form.interval_exec_time" @blur="checkTime" style="width:320px;" placeholder="请输入执行时间"></el-input>
                    <el-col class="cron_time_color">格式:时/分/秒,以(/)间隔</el-col>
                </el-form-item>
                <el-form-item v-if="form.exec_type !== '定时执行'" label="选择开始时间：" prop="start_time">
                    <el-date-picker
                            v-model="form.start_time"
                            type="datetime"
                            style="width:320px;"
                            placeholder="请选择任务开始时间"
                            value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                </el-form-item>
                <el-form-item v-if="form.exec_type !== '定时执行'" label="选择结束时间：" prop="end_time">
                    <el-date-picker
                            v-model="form.end_time"
                            type="datetime"
                            style="width:320px;"
                            placeholder="请选择任务结束时间"
                            value-format="yyyy-MM-dd HH:mm:ss">
                    </el-date-picker>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="CrontabVisible = false">取 消</el-button>
                <el-button type="primary" @click="timingExecScript">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 脚本立即执行弹出框 -->
        <el-dialog title="单机执行" :visible.sync="immediateExecVisible" width="40%" class="row-bg" :close-on-click-modal="false">
            <el-row v-for="item in scriptMessage" :key="item">
                <el-col :span="24" style="margin-top:10px;">
                    <span>{{ item }}</span>
                </el-col>
            </el-row>
        </el-dialog>
        <!-- 脚本批量执行弹出框 -->
        <el-dialog title="批量执行" :visible.sync="ExecVisible" width="60%" :close-on-click-modal="false">
            <el-row class="handle-box">
                <el-col :span="6" class="center">
                    <div>
                        <i style="font-size: 80px; font-weight: bold;" class="el-icon-document"></i>
                    </div>
                    <div>
                        <label class="blue">{{this.form.script_name}}</label>
                    </div>
                </el-col>
                <el-col :span="9">
                    <div>
                        执 行 人：{{this.username}}
                    </div>
                    <div>
                        脚本类型：{{this.form.script_type}}
                    </div>
                    <div>
                        脚本参数：{{this.form.param}}
                    </div>
                    <div>
                        执行主机：共 <label class="blue">{{rowLength}}</label> 台
                    </div>
                </el-col>
                <el-col :span="9">
                    <div>
                        开始时间: {{this.startFormatDate}}
                    </div>
                    <div>
                        结束时间: {{this.endFormatDate}}
                    </div>
                </el-col>
            </el-row>
            <el-table :data="this.scriptLogMessage">
                <el-table-column property="hostname" label="主机名称" width="200"></el-table-column>
                <el-table-column property="network_ip" label="内网IP"></el-table-column>
                <el-table-column property="username" label="账户"></el-table-column>
                <el-table-column property="execute_res" label="执行结果">
                    <template slot-scope="script_scope">
                        <div v-if="script_scope.row.execute_res">
                            <el-tag v-if="script_scope.row.execute_res==='执行中'">
                                <el-tooltip class="item" effect="dark" :content=script_scope.row.execute_res placement="top-start">
                                    <span>执行中</span>
                                </el-tooltip>
                            </el-tag>
                            <el-tag v-if="script_scope.row.execute_res==='已完成'" type="success">
                                <el-tooltip class="item" effect="dark" :content=script_scope.row.execute_res placement="top-start">
                                    <span>已完成</span>
                                </el-tooltip>
                            </el-tag>
                            <el-tag v-if="script_scope.row.execute_res.substr(0, 4)==='执行失败'" type="danger">
                                <el-tooltip class="item" effect="dark" :content=script_scope.row.execute_res placement="top-start">
                                    <span>执行失败</span>
                                </el-tooltip>
                            </el-tag>
                        </div>
                    </template>
                </el-table-column>
            </el-table>
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
            // const checkDate=(rule, value, callback) =>{
            //     const reg=/^([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)\s([0-9-,/*]+)$/;
            //     if(reg.test(value)==false){
            //         callback(new Error("请输入正确任务执行时间格式"));
            //     }
            // };
            // const checkTime=(rule, value, callback) =>{
            //     const reg=/^([0-1]?[0-9]|2[0-3])\/([0-5][0-9])\/([0-5][0-9])$/;
            //     if(reg.test(value)==false){
            //         callback(new Error("请输入正确任务执行时间格式"));
            //     }
            // };
            return {
                options: [],
                script_type_options: [
                    // {
                    //     value: '选项1',
                    //     label: 'Shell脚本'
                    // }, {
                    //     value: '选项2',
                    //     label: 'Python脚本'
                    // }, {
                    //     value: '选项3',
                    //     label: 'PERL脚本'
                    // }, {
                    //     value: '选项4',
                    //     label: 'JavaScript脚本'
                    // }
                ],
                script_category_options: [
                    // {
                    //     value: '选项1',
                    //     label: '浏览器脚本'
                    // }, {
                    //     value: '选项2',
                    //     label: '服务器脚本'
                    // }
                ],
                script_name_options: [],
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
                        value: '选项1',
                        label: '定时执行'
                    }, {
                        value: '选项2',
                        label: '周期性执行'
                    }, {
                        value: '选项3',
                        label: '轮巡执行'
                    }
                ],
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
                tableDataSelect: [],
                multipleSelection: [],
                delList: [],
                disabled: true,
                loading: true,
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
                    username: '',
                    exec_type:'',
                    exec_time:'',
                    cron_exec_time:'',
                    interval_exec_time:'',
                    exec_week:'',
                    start_time:'',
                    end_time:''
                },
                host_form: {},
                host: {},
                idx: -1,
                id: -1,
                rules: {
                    category: [
                        { required: true, message: '请选择脚本所属分类', trigger: 'change' }
                    ],
                    script_type: [
                        { required: true, message: '请选择脚本类型', trigger: 'change' }
                    ],
                    script_name: [
                        { required: true, message: '请选择脚本', trigger: 'change' }
                    ],
                    exec_type: [
                        { required: true, message: '请选择任务执行方式', trigger: 'change' }
                    ],
                    exec_time: [
                        { required: true, message: '请选择任务执行时间', trigger: 'change' }
                    ],
                    cron_exec_time: [
                        { required: true, message: '请输入任务执行时间', trigger: 'change' },
                        // { required: true, trigger: 'blur', validator: checkDate }
                    ],
                    interval_exec_time: [
                        { required: true, message: '请输入任务执行时间', trigger: 'change' },
                        // { required: true, trigger: 'blur', validator: checkTime }
                    ]
                },
                rowLength:0
            };
        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getScriptName();
        },
        methods: {
            formatPwd(row) {
                if(row.password) {
                    return '******'
                }
            },
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
                    // res.data.map( item =>{ item['network_ip']=item['network_ip'][0] });
                    this.tableData = res.data;
                    // this.pageTotal = res.data.total_count;
                    this.loading = false;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
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
            // 查询脚本信息
            getScriptName() {
                this.$http.get(`automation/api/script/?use=0`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    let obj_data=res.data;
                    let get_obj_name=[];
                    let get_obj_type=[];
                    let get_obj_category=[];
                    obj_data.map( item =>{
                        get_obj_name.push(item.script_name);
                        if (get_obj_type.indexOf(item.script_type)===-1){
                            get_obj_type.push(item.script_type);
                        }
                        if (get_obj_category.indexOf(item.category)===-1) {
                            get_obj_category.push(item.category);
                        }
                    });
                    this.script_name_options = get_obj_name;
                    this.script_type_options = get_obj_type;
                    this.script_category_options = get_obj_category;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发根据脚本所属分类搜索
            selectScriptByCategory(category) {
                this.$http.get(`automation/api/script?use=0&category=${category}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    let category_data=res.data;
                    let type_obj=[];
                    category_data.map( item =>{
                        if (type_obj.indexOf(item.script_type)===-1) {
                            type_obj.push(item.script_type);
                        }
                    });
                    this.script_type_options = type_obj;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发根据脚本类型搜索
            selectScriptByScriptType(script_type) {
                let url = this.url;
                if (this.form.category) {
                    url=`automation/api/script?use=0&category=${this.form.category}&scrip_type=${script_type}`
                }else {
                    url=`automation/api/script?use=0&scrip_type=${script_type}`
                }
                this.$http.get(url, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    let type_data=res.data;
                    let name_obj=[];
                    type_data.map( item =>{
                        if (name_obj.indexOf(item.script_name)===-1) {
                            name_obj.push(item.script_name);
                        }
                    });
                    this.script_name_options = name_obj;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发根据脚本名搜索
            selectScriptByScriptName(item) {
                this.$http.get(`automation/api/script?use=0&name=${item}`, {
                    headers:{
                        'token': this.token
                    }
                }).then((res)=>{
                    res.data[0].exec_type = '';
                    this.form = res.data[0];
                }).catch(  (error) => {
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
                if(this.multipleSelection.length===0) {
                    this.$message.warning('请选择要添加的主机！');
                }else {
                    if(this.tableDataSelect.length===0) {
                        this.tableDataSelect = this.multipleSelection;
                    }else {
                        this.tableDataSelect = this.tableDataSelect.concat(this.multipleSelection);
                    }
                    this.addHostVisible = false;
                    this.disabled = false;
                    this.rowLength=this.tableDataSelect.length;
                }
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
            //todo websocket方法合集
            initWebSocket() {
                // const token = sessionStorage.getItem('token');
                // const wsUrl = API_WEBSOCKET_URL + '/ws/clusterInfo' + ':' + token
                // if (this.websocket == null) {
                //     this.websocket = new WebSocket(wsUrl, [token])
                //     // this.websocket = new WebSocket(wsUrl,store('token'))
                // }
                // const wsUrl = this.globalAPI.websocketUrl + `ws/executing_script?uuid=${this.form.uuid}`
                console.log('wsUrl', this.wsUrl);
                if (this.websocket == null) {
                    this.websocket = new WebSocket(this.wsUrl)
                }
                //连接错误
                this.websocket.onerror = this.setErrorMessage

                // //连接成功
                this.websocket.onopen = this.setOnopenMessage

                //收到消息的回调
                this.websocket.onmessage = this.setOnmessageMessage

                //连接关闭的回调
                this.websocket.onclose = this.setOncloseMessage

                // 监听窗口关闭事件，当窗口关闭时，主动去关闭websocket连接，防止连接还没断开就关闭窗口，server端会抛异常。
                window.onbeforeunload = this.onbeforeunload
            },
            setErrorMessage() {
                console.log('WebSocket连接发生错误   状态码：' + this.websocket.readyState);
            },
            setOnopenMessage() {
                if(this.wsUrl === this.globalAPI.websocketUrl + `ws/immediate_exec_script/`) {
                    let actions = this.form;
                    this.websocket.send(JSON.stringify(actions));
                    console.log('WebSocket连接成功    状态码：' + this.websocket.readyState + actions);
                }else {
                    console.log('WebSocket连接成功    状态码：' + this.websocket.readyState);
                }
            },
            setOnmessageMessage(event) {
                console.log('event', event.data);
                // 根据服务器推送的消息做自己的业务处理
                var temp = ''
                try{
                    temp = JSON.parse(event.data);
                    this.scriptLogMessage = temp;
                }catch (e) {
                    temp = event.data;
                    this.scriptMessage.push(temp);
                }
            },
            setOncloseMessage() {
                console.log('WebSocket连接关闭    状态码：' + this.websocket.readyState);
                this.closeWebSocket();
                this.endFormatDate = getFormatDate();
                this.websocket = null;
            },
            onbeforeunload() {
                this.closeWebSocket()
            },
            closeWebSocket() {
                this.websocket.close()
            },
            genID(length){
                return Number(Math.random().toString().substr(3,length) + Date.now()).toString(36);
            },
            // 立即执行脚本
            immediateExecScript() {
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
            // 批量执行脚本
            batchExecScript() {
                if(this.form.script_name) {
                    this.form.host_info = this.tableDataSelect;
                    this.form.uuid = this.genID();
                    this.scriptLogMessage = this.tableDataSelect;
                    this.startFormatDate = getFormatDate();
                    this.endFormatDate = '--';
                    this.ExecVisible = true;
                    this.wsUrl = this.globalAPI.websocketUrl + `ws/executing_script?uuid=${this.form.uuid}`;
                    this.initWebSocket();
                    this.$http.post(`automation/api/script/exec_script/`,
                        this.form,
                        {
                            headers:{
                                'token': this.token,
                                'username': this.username
                            }
                        }).then((res)=>{
                        this.$message.success(res.data.msg);
                        // this.$router.push('/automation/script_log');
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else {
                    this.$message.warning('请选择脚本名称！');
                }
            },
            // 触发定时执行按钮
            handleCrontab() {
                if(this.form.script_name) {
                    this.CrontabVisible = true;
                    this.form.exec_type = '定时执行';
                    // this.getData();
                }else{
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
                if(this.form.exec_type !== '定时执行') {
                    var exec_end_time = this.execEndDatetimeFormat(this.form.end_time);
                    var now_time = this.execEndDatetimeFormat(getFormatDate());
                    if (this.form.end_time && exec_end_time < now_time) {
                        this.$message.warning('结束时间小于当前时间，请重新选择！');
                        return;
                    } else {
                        if (this.form.exec_type === '周期性执行') {
                            if (this.checkDate() === false) {
                                return;
                            }
                        } else if (this.form.exec_type === '轮巡执行') {
                            if (this.checkTime() === false) {
                                return;
                            }
                        }
                    }
                }
                this.form.host_info = this.tableDataSelect;
                this.form.uuid = this.genID();
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
            },
            // 格式化结束时间
            execEndDatetimeFormat(end_time){
                if(end_time!=null){
                    const dateMat = new Date(end_time);
                    return dateMat.getTime();
                }
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
        }
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

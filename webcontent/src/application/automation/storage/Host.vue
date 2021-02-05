<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 主机
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form ref="form">
                <el-form-item label="存储">
                    <el-select
                            v-model="storageHost"
                            filterable
                            remote
                            reserve-keyword
                            placeholder="请输入存储主机名称或IP"
                            :remote-method="queryHost"
                            class="selectIp"
                            @change="changeQueryHost">
                        <el-option
                                v-for="(item) in hostData"
                                :key=item.id
                                :label="`${item.hostname}/${item.manage_ip}`"
                                :value="item">
                        </el-option>
                    </el-select>
                </el-form-item>
            </el-form>
            <el-tabs v-model="activeIndex" @tab-click="handleStepOPtions">
                <el-tab-pane label="主机" name="1">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <el-col :span="17">
                            <div>
                                <el-button
                                        type="primary"
                                        @click="handleAddHost"
                                        class="handle-box"
                                >创建
                                </el-button>
                            </div>
                        </el-col>
                        <el-col :span="2">
                            <el-select v-model="SearchName">
                                <el-option label="名称" value="name"></el-option>
                                <el-option label="ID" value="id"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="3" class="mr10">
                            <el-input v-model="hostnameSearch" v-if="SearchName==='name'" placeholder="关键字" clearable></el-input>
                            <el-input v-model="hostidSearch" v-if="SearchName==='id'" placeholder="关键字" clearable></el-input>
                        </el-col>
                        <el-col :span="2">
                            <el-button size="small" @click="querySearchHost">搜索</el-button>
                        </el-col>
                    </el-row>
                    <el-table
                            v-loading="hostloading"
                            element-loading-text="拼命加载中"
                            element-loading-spinner="el-icon-loading"
                            :data="tableData"
                            border
                            style="width: 100%"
                    >
<!--                        <af-table-column prop="TYPE" label="类型" align="center" :formatter="handletype"></af-table-column>-->
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="IP" label="IP地址" align="center"></af-table-column>
                        <af-table-column prop="OPERATIONSYSTEM" label="主机操作系统" align="center" :formatter="handleoperationsystem"></af-table-column>
                        <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                        <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
<!--                        <af-table-column prop="LOCATION" label="位置" align="center"></af-table-column>-->
                        <af-table-column prop="ISADD2HOSTGROUP" label="是否已添加给HostGroup" :formatter="handlefy" align="center"></af-table-column>
                        <af-table-column prop="INITIATORNUM" label="主机启动器数量" align="center"></af-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="主机组" name="2">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <el-col :span="17">
                            <div>
                                <el-button
                                        type="primary"
                                        @click="handleAddHostGroup"
                                        class="handle-box"
                                >创建
                                </el-button>
                            </div>
                        </el-col>
                        <el-col :span="2">
                            <el-select v-model="groupSearchName">
                                <el-option label="名称" value="name"></el-option>
                                <el-option label="ID" value="id"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="3" class="mr10">
                            <el-input v-model="hostgroupnameSearch" v-if="groupSearchName==='name'" placeholder="关键字" clearable></el-input>
                            <el-input v-model="hostgroupidSearch" v-if="groupSearchName==='id'" placeholder="关键字" clearable></el-input>
                        </el-col>
                        <el-col :span="2">
                            <el-button size="small" @click="querySearchHostgroup">搜索</el-button>
                        </el-col>
                    </el-row>
                    <el-table
                            v-loading="hostloading"
                            element-loading-text="拼命加载中"
                            element-loading-spinner="el-icon-loading"
                            :data="hostGrouptableData"
                            highlight-current-row
                            border
                            style="width: 100%"
                            @current-change="handleShowHostGroup"
                    >
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                    </el-table>
                    <el-divider></el-divider>
                    <el-table
                            :data="selectedHostGroupTableData"
                            border
                            style="width: 100%"
                    >
                        <af-table-column prop="TYPE" label="类型" align="center" :formatter="handletype"></af-table-column>
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="IP" label="IP地址" align="center"></af-table-column>
                        <af-table-column prop="OPERATIONSYSTEM" label="主机操作系统" align="center" :formatter="handleoperationsystem"></af-table-column>
                        <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                        <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                        <af-table-column prop="LOCATION" label="位置" align="center"></af-table-column>
                        <af-table-column prop="ISADD2HOSTGROUP" label="是否已添加给HostGroup" :formatter="handlefy" align="center"></af-table-column>
                        <af-table-column prop="INITIATORNUM" label="主机启动器数量" align="center"></af-table-column>
                    </el-table>
                </el-tab-pane>
            </el-tabs>
        </div>
        <!--新增主机-->
        <el-dialog :title="title" :visible.sync="addHostVisible" width="35%">
            <el-form ref="hostform" :rules="hostrules" :model="hostform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="hostform.NAME" style="width: 250px;"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="hostform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-form-item label="操作系统" prop="OPERATIONSYSTEM">
                    <el-select v-model="hostform.OPERATIONSYSTEM" style="width: 250px;">
                        <el-option label="Linux" value="0"></el-option>
                        <el-option label="Windows" value="1"></el-option>
                        <el-option label="Solaris" value="2"></el-option>
                        <el-option label="HP-UX" value="3"></el-option>
                        <el-option label="AIX" value="4"></el-option>
                        <el-option label="XenServer" value="5"></el-option>
                        <el-option label="Mac OS" value="6"></el-option>
                        <el-option label="VMware ESX" value="7"></el-option>
                        <el-option label="LINUX_VIS" value="8"></el-option>
                        <el-option label="Windows Server 2012" value="9"></el-option>
                        <el-option label="Oracle VM" value="10"></el-option>
                        <el-option label="OpenVMS" value="11"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="设备位置">
                    <el-input v-model="hostform.LOCATION" style="width: 250px;"></el-input>
                </el-form-item>
                <el-form-item label="数量" prop="luncount">
                    <el-row>
                        <el-input v-model="hostcount" type="number" style="width: 250px;" @input="handehostcount"></el-input>
                    </el-row>
                    <el-row>
                        <el-checkbox v-model="hostcountchecked" :disabled="hostcountdisabled" @change="handlestartunit">手动指定后缀编号</el-checkbox>
                    </el-row>
                    <el-row>
                        <el-col :span="13">
                            <el-form-item label="起始编号" v-if="startnumbershow" prop="startnumber">
                                <el-input v-model="startnumber" type="number" style="width: 100px;" @input="handlestartnumber"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <span v-if="startnumbershow">(0~{{10000-hostcount}})</span>
                        </el-col>
                    </el-row>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHostVisible=false">取 消</el-button>
                <el-button type="primary" @click="handlePrompt">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="危险" :visible.sync="promptVisible" width="30%">
            <div class="prompt-border">
                <span>
                    1、执行该操作前，请确认待创建主机的操作系统类型与业<br/>务主机操作系统类型是否一致。<br/>
                    2、若业务主机操作系统为Windows，并且需要使用thin<br/>LUN的完整功能以得到更好的体验，请选择Windows<br/>
                    Server 2012。<br/>
                    建议：请再次确认指定了正确的操作系统类型。
                </span>
            </div>
            <el-row style="margin-top: 10px;">
                <el-checkbox v-model="hostSelectChecked" @change="handleCheckSelect">我已阅读上述信息，了解执行此操作带来的后果。</el-checkbox>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="promptVisible = false">取 消</el-button>
                <el-button type="primary" :disabled="hostSelectDisabled" @click="saveAddHostList">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="执行结果" :visible.sync="addresultVisible" width="30%">
            <el-table
                    :data="resultData"
                    border
                    style="width: 100%"
            >
                <af-table-column prop="name" label="操作" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="reason" label="失败原因和建议" align="center"></af-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addresult">关闭</el-button>
            </span>
        </el-dialog>
        <!--创建主机组弹出框-->
        <el-dialog title="创建主机组" :visible.sync="addHostGroupVisible" width="77%">
            <el-form ref="hostgroupform" :rules="hostGroupRules" :model="hostgroupform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="hostgroupform.NAME"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="hostgroupform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-row>
                    <el-col :span="11">
                        <p class="lungroup_create_p">可选主机</p>
                        <el-row type="flex" class="row-bg margin_bot" justify="end">
                            <el-col :span="6">
                                <el-select v-model="leftSearchName">
                                    <el-option label="名称" value="name"></el-option>
                                    <el-option label="ID" value="id"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-input v-model="leftnameSearch" v-if="leftSearchName==='name'" placeholder="关键字" clearable></el-input>
                                <el-input v-model="leftidSearch" v-if="leftSearchName==='id'" placeholder="关键字" clearable></el-input>
                            </el-col>
                            <el-col :span="3">
                                <el-button size="small" @click="querySearchleft">搜索</el-button>
                            </el-col>
                        </el-row>
                        <div class="trans_table_cls">
                            <el-table
                                    ref="hostTable"
                                    :key="tableKey"
                                    :row-key="getRowKeys"
                                    :data="noGroupTableData"
                                    border
                                    fit
                                    highlight-current-row
                                    @selection-change="handleHostGroupChange"
                                    class="margin_bot"
                            >
                                <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                                <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                                <af-table-column prop="RUNNINGSTATUS" label="状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                                <af-table-column prop="OPERATIONSYSTEM" label="操作系统" align="center" :formatter="handleoperationsystem"></af-table-column>
                                <af-table-column prop="IP" label="IP地址" align="center"></af-table-column>
                                <af-table-column prop="ISADD2HOSTGROUP" label="已归属主机" align="center" :formatter="handlefy"></af-table-column>
                            </el-table>
                        </div>
                        <el-checkbox label="仅显示未归属于主机组的主机" :value="isAddToHostGroup" @change="handleSelectAddToHostGroup" style="margin-top: 6px;"></el-checkbox>
                    </el-col>
                    <el-col :span="2" class="trans_button_cls">
                        <el-button
                                @click="addHost"
                                type="primary"
                                :disabled="!hostGroupData.length"
                                icon="el-icon-arrow-right"
                                circle
                        ></el-button>
                        <br>
                        <el-button
                                @click="removeHost"
                                type="primary"
                                :disabled="!selectedHostList.length"
                                icon="el-icon-arrow-left"
                                circle
                                style="margin-left: 0;margin-top: 10px;"
                        ></el-button>
                    </el-col>
                    <el-col :span="11">
                        <p class="lungroup_create_p">已选主机</p>
                        <el-row type="flex" class="row-bg margin_bot" justify="end">
                            <el-col :span="6">
                                <el-select v-model="rightSearchName">
                                    <el-option label="名称" value="name"></el-option>
                                    <el-option label="ID" value="id"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-input v-model="rightnameSearch" v-if="rightSearchName==='name'" placeholder="关键字" clearable></el-input>
                                <el-input v-model="rightidSearch" v-if="rightSearchName==='id'" placeholder="关键字" clearable></el-input>
                            </el-col>
                            <el-col :span="3">
                                <el-button size="small" @click="querySearchright">搜索</el-button>
                            </el-col>
                        </el-row>
                        <div class="trans_table_cls">
                            <el-table
                                    ref="selectedHostTable"
                                    :key="tableKey"
                                    :row-key="getRowKeys"
                                    :data="selectedHostTableData"
                                    border
                                    fit
                                    highlight-current-row
                                    @selection-change="handleSelectedHostChange"
                            >
                                <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                                <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                                <af-table-column prop="RUNNINGSTATUS" label="状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                                <af-table-column prop="OPERATIONSYSTEM" label="操作系统" align="center" :formatter="handleoperationsystem"></af-table-column>
                                <af-table-column prop="IP" label="IP地址" align="center"></af-table-column>
                                <af-table-column prop="ISADD2HOSTGROUP" label="已归属主机" align="center" :formatter="handlefy"></af-table-column>
                            </el-table>
                        </div>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHostGroupVisible = false">取 消</el-button>
                <el-button type="primary" @click="createHostGroup">确 定</el-button>
            </span>
        </el-dialog>
        <!--创建主机组执行结果弹框-->
        <el-dialog title="执行结果" :visible.sync="addHostGroupResultVisible" width="30%">
            <el-table
                    :data="hostGroupResultData"
                    border
                    style="width: 100%"
            >
                <af-table-column prop="name" label="操作" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="reason" label="失败原因和建议" align="center"></af-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addHostGroupResult">关闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "HostGroup",
        data() {
            return {
                active:0,
                title: '创建主机',
                storageHost: '',
                activeIndex: '1',
                tableData: [], // 查询一条存储返回的数据
                copytableData: [],
                hostGrouptableData: [],
                selectedHostTableData: [],
                selectedHostGroupTableData: [],
                hostGroupResultData: [],
                hostData: [],
                resultData: [],
                hostGroupSearchName: '',
                hostGroupSearchValue: '',
                addHostVisible: false, // 创建时弹框的设置
                addotherVisible:false, // 创建增加启动器时的弹框设置
                addresultVisible:false,
                addHostGroupVisible: false,
                addHostGroupResultVisible: false,
                promptVisible: false,
                warningVisible: false, // 创建时的警告弹框信息设置
                addFlag: false,
                hostSelectChecked: false,
                hostSelectDisabled: true,
                isAddToHostGroup: true,
                hostform: {}, // 创建时传的参数
                hostgroupform: {},
                hostcount: 1,
                startnumber: 0,
                tableKey: 0,
                hostGroupData: [],
                selectedHostList: [],
                noGroupTableData: [],
                selectHostTableData: [],
                ISADD2HOSTGROUP: false,
                startnumbershow: false,
                hostcountchecked: false,
                hostcountdisabled: true,
                hostloading: false,
                storage_env: '',
                hostrules: {
                    NAME: [
                        { required: true, message: '请输入名称'},
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ],
                    OPERATIONSYSTEM: [
                        {required: true, message: '请选择操作系统', trigger: 'blur'}
                    ],
                    startnumber: [
                        {required: true, message: '请选输入起始编号', trigger: 'blur'}
                    ]
                },
                hostGroupRules: {
                    NAME: [
                        { required: true, message: '请输入主机组名称', trigger: 'blur' },
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ]
                },
                SearchName: 'name',
                hostnameSearch: '',
                hostidSearch: '',
                groupSearchName: 'name',
                hostgroupnameSearch: '',
                hostgroupidSearch: '',
                copyhostGrouptableData: [],
                rightSearchName: 'name',
                leftSearchName: 'name',
                leftnameSearch: '',
                rightnameSearch: "",
                leftidSearch: '',
                rightidSearch: '',
                copynoGroupTableData: [],
                copyselectedHostTableData: []

            }
        },
        created() {
            this.getData();
        },
        methods: {
            // 实时查询存储
            queryHost(query){
                this.$http.get(`asset/api/storage/storage/?query=${query}`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.hostData = res.data;
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            changeQueryHost(row) {
                sessionStorage.setItem('storage_env', JSON.stringify(row));
                this.storage_env = row;
                this.tableData = [];
                this.storageHost = row.hostname + '/' + row.manage_ip;
                this.hostGrouptableData = [];
                if(this.activeIndex==='1'){
                    this.getHostList();
                }else{
                    this.getHostGroupList();
                }
            },
            // 查询主机信息
            getHostList(){
                console.log(this.storage_env, 666666)
                this.hostloading = true
                this.$http.post( `automation/api/storage/host_list/`, this.storage_env,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data;
                    this.copytableData = this.tableData;
                    this.hostloading = false;
                    this.getNoAddToHostGroupList();
                }).catch( (error) => {
                    this.hostloading = false;
                    this.$message.error(JSON.stringify(error.response.data.msg));
                });
            },
            // 查询未归属主机组主机信息
            getNoAddToHostGroupList(){
                this.$http.post( `automation/api/storage/host_list/?ISADD2HOSTGROUP=false`, this.storage_env,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.noGroupTableData = res.data;
                    this.copynoGroupTableData = this.noGroupTableData
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            getData() {
                this.$http.get(`asset/api/storage/?current_page=1&pre_page=1`,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    if(res.data['data'].length != 0){
                        if(sessionStorage.getItem('storage_env')) {
                            this.storage_env = JSON.parse(sessionStorage.getItem('storage_env'));
                        }else {
                            sessionStorage.setItem('storage_env', JSON.stringify(res.data['data'][0]));
                            this.storage_env = res.data['data'][0];
                        }
                        // this.storage_env = res.data['data'][0];
                        this.storageHost = this.storage_env['hostname'] + '/' + this.storage_env['manage_ip'];
                        this.getHostList();
                    }else{
                        this.$message.error("未发现存储环境!")
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 点击选项操作
            handleStepOPtions(tab){
                if(tab.name==='1'){
                    this.getHostList();
                }else{
                    this.getHostGroupList();
                }
            },
            // 查询主机组
            getHostGroupList(){
                this.$http.post( `automation/api/storage/host_group_list/`, this.storage_env,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.hostGrouptableData = res.data['data'];
                    this.copyhostGrouptableData = this.hostGrouptableData
                    this.hostloading = false
                }).catch( (error) => {
                    this.hostloading = false
                    this.$message.error(JSON.stringify(error.response.data.msg))
                });
            },
            resetCreate(){
                this.warningVisible=false;
            },
            // 处理创建主机
            handleAdd(){
                this.hostform = {}
                this.addHostVisible = true;
            },
            // 处理数量大于1的情况
            handehostcount(res){
                this.hostcountchecked = false;
                if(res>1){
                    this.hostcountdisabled = false;
                }else{
                    this.hostcountdisabled = true;
                    this.startnumbershow = false;
                }
            },
            //处理起始编号
            handlestartunit(){
                this.startnumbershow = !this.startnumbershow
            },
            // 处理开始编号
            handlestartnumber(res){
                this.resultData = []
                for (var i=0;i<this.luncount;i++)
                {
                    let id_len = res.toString().length
                    let name = ''
                    let real_name = ''
                    if(id_len===1){
                        real_name = this.lunform.NAME + '000' + res
                        name = "创建LUN " + real_name
                    }else if(id_len===2){
                        real_name = this.lunform.NAME + '00' + res
                        name = "创建LUN " + real_name
                    }else if(id_len===3) {
                        real_name = this.lunform.NAME + '0' + res
                        name = "创建LUN " + real_name
                    }else{
                        real_name = this.lunform.NAME + res
                        name = "创建LUN " + real_name
                    }
                    this.resultData.push({'name': name, 'status': '等待执行', 'reason': '', 'real_name': real_name})
                    res = parseInt(res) + 1
                }
            },
            // 处理选中操作
            handleCheckSelect() {
                this.hostSelectDisabled = !this.hostSelectDisabled;
            },
            // 处理创建主机
            handleAddHost(){
                this.hostform = {
                    DESCRIPTION: '',
                    LOCATION: '',
                    OPERATIONSYSTEM: 'Linux'
                };
                this.hostSelectChecked = false;
                this.hostSelectDisabled = true;
                this.hostcount = 1
                this.hostcountdisabled = true
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                this.$http.post(`automation/api/storage/nextavailableid/?type=21`,
                    this.storage_env,
                    {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    let avaliableid = res['data']['ID']
                    avaliableid = parseInt(avaliableid) + 1
                    let id_len = avaliableid.toString().length
                    if (id_len === 1) {
                        this.$set(this.hostform, 'NAME', 'Host00' + avaliableid)
                    } else if (id_len === 2) {
                        this.$set(this.hostform, 'NAME', 'Host0' + avaliableid)
                    } else {
                        this.$set(this.hostform, 'NAME', 'Host' + avaliableid)
                    }
                    loading.close();
                    this.addHostVisible = true;
                }).catch((error) => {
                    loading.close();
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 处理提示框
            handlePrompt() {
                this.promptVisible = true;
            },
            // 添加主机操作
            saveAddHostList(){
                this.promptVisible = false;
                const CustomForeach = async (arr, callback) => {
                    const length = arr.length;
                    const O = Object(arr);
                    let k = 0;
                    while (k < length) {
                        if (k in O) {
                            const kValue = O[k];
                            await callback(kValue, k, O);
                        }
                        k++;
                    }
                };
                this.addresultVisible = true;
                console.log(this.hostcount, this.resultData, 111)
                if(this.hostcount===1){
                    this.resultData = [];
                    let add_res = {'name': this.hostform.NAME, 'status': '正在执行', 'reason': '', 'real_name': this.hostform.NAME};
                    this.resultData.push(add_res);
                    this.saveAddHost(add_res);
                }else{
                    if(this.resultData.length!=0){
                        CustomForeach(this.resultData, async (e) => {
                            await this.saveAddHost(e);
                        })}else{
                        for (var i=0;i<this.hostcount;i++)
                        {
                            let id_len = i.toString().length
                            let name = ''
                            let real_name = ''
                            if(id_len===1){
                                real_name = this.hostform.NAME + '000' + i
                                name = "创建Host " + real_name
                            }else if(id_len===2){
                                real_name = this.hostform.NAME + '00' + i
                                name = "创建Host " + real_name
                            }else if(id_len===3) {
                                real_name = this.hostform.NAME + '0' + i
                                name = "创建Host " + real_name
                            }else{
                                real_name = this.hostform.NAME + i
                                name = "创建Host " + real_name
                            }
                            this.resultData.push({'name': name, 'status': '等待执行', 'reason': '', 'real_name': real_name})
                        }
                        CustomForeach(this.resultData, async (e) => {
                            await this.saveAddHost(e);
                        });
                    }
                }
            },
            saveAddHost(add_res){
                if(this.hostform.OPERATIONSYSTEM==='Linux') {
                    this.hostform.OPERATIONSYSTEM=0;
                }
                return new Promise((resolve, reject) => {
                    this.hostform.NAME = add_res.real_name;
                    add_res.status = '正在执行'
                    this.$http.post(`automation/api/storage/create_host/`,
                        {data: this.hostform, storage_env: this.storage_env}, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        if(res.status===200){
                            add_res.status = '成功';
                        }else{
                            add_res.status = '执行失败';
                            add_res.reason = res.data;
                        }
                        resolve(res)
                    }).catch( (error)=> {
                        reject(error)
                        this.$message.error(JSON.stringify(error.response.data));
                        add_res.status = '执行出错';
                        add_res.reason = error.response.data.msg.description;
                    });
                })
            },
            //执行结果点击关闭时
            addresult(){
                this.addresultVisible = false;
                this.addHostVisible = false;
                this.getHostList();
            },
            // 获得当前行
            getRowKeys(row) {
                return row.NAME;
            },
            // 选中值操作
            handleHostGroupChange(rows){
                this.hostGroupData = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.hostGroupData.push(row);
                        }
                    });
                }
            },
            // 将右边表格选择项存入selectedStaffData中
            handleSelectedHostChange(rows){
                this.selectedHostList = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.selectedHostList.push(row);
                        }
                    });
                }
            },
            // 处理创建主机组
            handleAddHostGroup(){
                this.hostgroupform = {
                    DESCRIPTION: ''
                };
                this.selectedHostTableData = []
                this.copyselectedHostTableData = []
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                this.$http.post(`automation/api/storage/nextavailableid/?type=14`,
                    this.storage_env,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    let avaliableid = res['data']['ID']
                    avaliableid = parseInt(avaliableid) + 1
                    let id_len = avaliableid.toString().length
                    if (id_len === 1) {
                        this.$set(this.hostgroupform, 'NAME', 'HostGroup00' + avaliableid)
                    } else if (id_len === 2) {
                        this.$set(this.hostgroupform, 'NAME', 'HostGroup0' + avaliableid)
                    } else {
                        this.$set(this.hostgroupform, 'NAME', 'HostGroup' + avaliableid)
                    }
                    loading.close();
                    this.addHostGroupVisible = true;
                }).catch((error) => {
                    loading.close();
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 选择显示归属主机组
            handleSelectAddToHostGroup() {
                this.isAddToHostGroup = !this.isAddToHostGroup;
                if(this.isAddToHostGroup) {
                    this.$http.post( `automation/api/storage/host_list/?ISADD2HOSTGROUP=0`, this.storage_env,{
                        headers:{
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.noGroupTableData = res.data;
                        this.copynoGroupTableData = this.noGroupTableData
                        for (let i = 0; i < this.copyselectedHostTableData.length; i++) {
                            for (let j = 0; j < this.noGroupTableData.length; j++) {
                                if (
                                    this.copyselectedHostTableData[i] &&
                                    this.noGroupTableData[j] &&
                                    this.copyselectedHostTableData[i].NAME === this.noGroupTableData[j].NAME
                                ) {
                                    this.noGroupTableData.splice(j, 1);
                                }
                            }
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else {
                    this.$http.post( `automation/api/storage/host_list/`, this.storage_env,{
                        headers:{
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.noGroupTableData = res.data;
                        this.copynoGroupTableData = this.noGroupTableData
                        for (let i = 0; i < this.copyselectedHostTableData.length; i++) {
                            for (let j = 0; j < this.noGroupTableData.length; j++) {
                                if (
                                    this.copyselectedHostTableData[i] &&
                                    this.noGroupTableData[j] &&
                                    this.copyselectedHostTableData[i].NAME === this.noGroupTableData[j].NAME
                                ) {
                                    this.noGroupTableData.splice(j, 1);
                                }
                            }
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }
            },
            // 左边表格选择项移到右边
            addHost() {
                setTimeout(() => {
                    this.$refs["hostTable"].clearSelection();
                    this.$refs["selectedHostTable"].clearSelection();
                }, 0);
                this.hostGroupData.forEach(item => {
                    this.selectedHostTableData.push(item);
                });
                this.copyselectedHostTableData = this.selectedHostTableData
                for (let i = this.noGroupTableData.length-1; i >= 0; i--) {
                    for (let j = 0; j < this.hostGroupData.length; j++) {
                        if (
                            this.noGroupTableData[i] &&
                            this.hostGroupData[j] &&
                            this.noGroupTableData[i].NAME === this.hostGroupData[j].NAME
                        ) {
                            this.noGroupTableData.splice(i, 1);
                        }
                    }
                }
                this.copynoGroupTableData = this.noGroupTableData
            },
            // 右边表格选择项移到左边
            removeHost() {
                setTimeout(() => {
                    this.$refs["hostTable"].clearSelection();
                    this.$refs["selectedHostTable"].clearSelection();
                }, 0);
                this.selectedHostList.forEach(item => {
                    this.noGroupTableData.push(item);
                });
                this.copynoGroupTableData = this.noGroupTableData
                for (let i = this.selectedHostTableData.length-1; i >=0 ; i--) {
                    for (let j = 0; j < this.selectedHostList.length; j++) {
                        if (
                            this.selectedHostTableData[i] &&
                            this.selectedHostList[j] &&
                            this.selectedHostTableData[i].NAME === this.selectedHostList[j].NAME
                        ) {
                            this.selectedHostTableData.splice(i, 1);
                        }
                    }
                }
            },
            // 创建主机组并添加主机
            createHostGroup(){
                this.hostGroupResultData = [];
                let name = "创建主机组 " + this.hostgroupform.NAME;
                let add_res = {'name': name, 'status': '正在执行', 'reason': ''}
                this.hostGroupResultData.push(add_res)
                for (var i=0;i<this.selectedHostTableData.length;i++)
                {
                    let host_name = "增加主机 " + this.selectedHostTableData[i].NAME;
                    this.hostGroupResultData.push({'name': host_name, 'status': '等待执行', 'reason': '','host_id': this.selectedHostTableData[i].ID});
                }
                this.addHostGroupResultVisible = true;
                this.create_host_group();
            },
            // 创建主机组
            create_host_group(){
                const CustomForeach = async (arr, callback) => {
                    const length = arr.length;
                    const O = Object(arr);
                    let k = 0;
                    while (k < length) {
                        if (k in O) {
                            console.log('doing foreach...');
                            const kValue = O[k];
                            await callback(kValue, k, O);
                        }
                        k++;
                    }
                };
                this.$http.post(`automation/api/storage/create_host_group/`,
                    {'data': this.hostgroupform,'storage_env': this.storage_env}, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let host_group_data = res.data.data;
                    if(res.status===200){
                        this.hostGroupResultData[0].status = '成功';
                    }else{
                        this.hostGroupResultData[0].status = '执行失败';
                        this.hostGroupResultData[0].reason = res.data;
                    }
                    if(host_group_data){
                        CustomForeach(this.hostGroupResultData, async (e, i) => {
                            if(i>0){
                                await this.hostGrouPassociate(e, host_group_data.ID);
                            }
                        });
                    }
                }).catch((error) =>{
                    this.hostGroupResultData[0].status = '执行失败';
                    this.hostGroupResultData[0].reason = error.response.data.msg
                    this.$message.error(JSON.stringify(error.response.data.msg));
                })
            },
            // 主机组添加主机
            hostGrouPassociate(add_res, group_id){
                return new Promise((resolve, reject) => {
                    this.hostgroupform.NAME = add_res.real_name;
                    add_res.status = '正在执行';
                    this.$http.post(`automation/api/storage/host_group_associate/`, {
                        'data':{'ID': group_id, "ASSOCIATEOBJTYPE": 21, "ASSOCIATEOBJID": add_res.host_id}, 'storage_env': this.storage_env
                    }, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        if(res.status===200){
                            add_res.status = '成功';
                        }else{
                            add_res.status = '执行失败';
                            add_res.reason = res.data;
                        }
                        resolve(res);
                    }).catch( (error)=> {
                        reject(error);
                        add_res.status = '执行失败';
                        add_res.reason = error.response.data.msg;
                        this.$message.error(JSON.stringify(error.response.data.msg));
                    });
                })
            },
            // 关闭创建主机组弹框
            addHostGroupResult(){
                this.addHostGroupResultVisible = false
                this.addHostGroupVisible = false
                this.getHostGroupList()
            },
            // 点击展示主机组内主机信息
            handleShowHostGroup(row) {
                this.$http.post(`automation/api/storage/associate_group/?TYPE=21&ASSOCIATEOBJTYPE=${row.TYPE}&ASSOCIATEOBJID=${row.ID}`, {
                    'manage_address': this.storage_env.manage_address,
                    'manage_username': this.storage_env.manage_username,
                    'manage_password': this.storage_env.manage_password
                }, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if(res.data) {
                        this.selectedHostGroupTableData = res.data;
                    }else {
                        this.selectedHostGroupTableData = [];
                    }
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data.msg));
                    this.grouptableData = [];
                });
            },
            handletype(row){
                return row.TYPE == '21' ? '主机' : '';
            },
            handlefy(row){
                return row.ISADD2HOSTGROUP == 'false' ? '否' : row.ISADD2HOSTGROUP == 'true' ? '是' : ''
            },
            //处理运行状态
            handlerunningstatus(row){
                return row.RUNNINGSTATUS == '1' ? '正常': '';
            },
            //处理健康状态
            handlehealthstatus(row){
                return row.HEALTHSTATUS == '1' ? '正常' : row.HEALTHSTATUS == '17' ? '无冗余': '';
            },
            // 处理操作系统
            handleoperationsystem(row){
                return row.OPERATIONSYSTEM == '0' ? 'linux' :row.OPERATIONSYSTEM == '1' ? 'Windows'
                    :row.OPERATIONSYSTEM == '2' ? 'Solaris' : row.OPERATIONSYSTEM == '3' ? 'HP-UX'
                        :row.OPERATIONSYSTEM == '4' ? 'AIX' : row.OPERATIONSYSTEM == '5' ? 'XenServer'
                            :row.OPERATIONSYSTEM == '6' ? 'Mac OS' : row.OPERATIONSYSTEM == '7' ? 'VMware ESX'
                                : row.OPERATIONSYSTEM == '8' ? 'LINUX_VIS' : row.OPERATIONSYSTEM == '9' ? 'Windows Server 2012'
                                    : row.OPERATIONSYSTEM == '10' ? 'Oracle VM' : row.OPERATIONSYSTEM == '11' ? 'OpenVMS'
                                        : ''
            },
            querySearchHost(){
                if(this.SearchName==='name'){
                    if(this.hostnameSearch!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.hostnameSearch);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }else if(this.SearchName==='id'){
                    if(this.hostidSearch!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.hostidSearch);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }
            },
            querySearchHostgroup(){
                if(this.groupSearchName==='name'){
                    if(this.hostgroupnameSearch!=''){
                        this.hostGrouptableData = []
                        this.copyhostGrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.hostgroupnameSearch);
                            if(incledes_res===true){
                                this.hostGrouptableData.push(item)
                            }
                        })
                    }else{
                        this.hostGrouptableData = this.copyhostGrouptableData
                    }
                }else if(this.groupSearchName==='id'){
                    if(this.hostgroupidSearch!=''){
                        this.hostGrouptableData = []
                        this.copyhostGrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.hostgroupidSearch);
                            if(incledes_res===true){
                                this.hostGrouptableData.push(item)
                            }
                        })
                    }else{
                        this.hostGrouptableData = this.copyhostGrouptableData
                    }
                }
            },
            querySearchleft(){
                if(this.leftSearchName==='name'){
                    if(this.leftnameSearch!=''){
                        this.noGroupTableData = []
                        this.copynoGroupTableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.leftnameSearch);
                            if(incledes_res===true){
                                this.noGroupTableData.push(item)
                            }
                        })
                    }else{
                        this.noGroupTableData = this.copynoGroupTableData
                    }
                }else if(this.leftSearchName==='id'){
                    if(this.leftidSearch!=''){
                        this.noGroupTableData = []
                        this.copynoGroupTableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.leftidSearch);
                            if(incledes_res===true){
                                this.noGroupTableData.push(item)
                            }
                        })
                    }else{
                        this.noGroupTableData = this.copynoGroupTableData
                    }
                }
            },
            querySearchright(){
                console.log(this.selectedHostTableData, 5555)
                console.log(this.rightSearchName)
                // coonsole.log(this.rightnameSearch)
                if(this.rightSearchName==='name'){
                    if(this.rightnameSearch!=''){
                        this.selectedHostTableData = []
                        this.copyselectedHostTableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.rightnameSearch);
                            if(incledes_res===true){
                                this.selectedHostTableData.push(item)
                            }
                        })
                    }else{
                        this.selectedHostTableData = this.copyselectedHostTableData
                    }
                }else if(this.rightSearchName==='id'){
                    if(this.rightidSearch!=''){
                        this.selectedHostTableData = []
                        this.copyselectedHostTableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.rightidSearch);
                            if(incledes_res===true){
                                this.selectedHostTableData.push(item)
                            }
                        })
                    }else{
                        this.selectedHostTableData = this.copyselectedHostTableData
                    }
                }
            }
        }
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
        width: 200px;
        display: inline-block;
    }
    .table-width {
        word-break: keep-all;
        white-space: nowrap;
    }
    .margin_bot{
        margin-bottom: 10px;
    }
    .create-input {
        width: 260px;
    }
    .prompt-border {
        height: 130px;
        padding: 10px;
        border: 1px solid #c5c3c3
    }
    .trans_button_cls{
        text-align: center;
        margin-top: 15%;
    }
    .trans_table_cls{
        height: 200px;
        overflow: auto;
    }
    .lungroup_create_p{
        border-bottom: 1px solid #C0C4CC;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }
</style>

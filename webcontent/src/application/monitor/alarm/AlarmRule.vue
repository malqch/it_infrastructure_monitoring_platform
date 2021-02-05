<template>
    <div>
        <div class="wrapper">
            <!--<div class="crumbs">
                <el-breadcrumb separator="/">
                    <el-breadcrumb-item>
                        <i class="el-icon-lx-cascades"></i> 告警规则管理
                    </el-breadcrumb-item>
                </el-breadcrumb>
            </div>-->
            <div class="container">
                <el-form :inline="true" v-model="form">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <div>
                            <!--cpu使用率-->
                            <el-button
                                    type="success"
                                    icon="el-icon-circle-plus-outline"
                                    @click="settingFile()"
                                    class="handle-box-1"
                            >添加规则
                            </el-button>
                        </div>
                        <div type="flex" class="row-bg" justify="end">
                            <el-form-item>
                                <el-input v-model="searchData.rule_name" clearable placeholder="告警规则名称" class="handle-input"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="searchData.device_name" clearable placeholder="设备名称" class="handle-input"></el-input>
                            </el-form-item>
                            <el-form-item>
                                <el-input v-model="searchData.device_ip" clearable placeholder="ip" class="handle-input"></el-input>
                            </el-form-item>
                            <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                        </div>
                    </el-row>
                </el-form>
                <el-table
                        :data="tableData"
                        border
                        ref="multipleTable"
                        header-cell-class-name="table-header"
                        @selection-change="handleSelectionChange"
                >
                    <el-table-column type="index" label="序号" align="center"></el-table-column>
                    <el-table-column prop="rule_name" label="告警规则名称" align="center"></el-table-column>
                    <el-table-column prop="tag" label="标签" align="center" width="250"></el-table-column>
                    <el-table-column prop="device_name" label="设备名称" align="center"></el-table-column>
                    <el-table-column prop="alarm_object" label="告警类型" align="center"></el-table-column>
                    <el-table-column prop="create_time" :formatter="dateFormat" label="创建时间" align="center" :show-overflow-tooltip=true width="150"></el-table-column>
                    <el-table-column prop="update_time" :formatter="dateFormat" label="更新时间" align="center" :show-overflow-tooltip=true width="150"></el-table-column>
                    <el-table-column label="操作"  align="center" width="150">
                        <template slot-scope="scope">
                            <el-button
                                    type="text"
                                    icon="el-icon-edit"
                                    @click="handleEdit(scope.row)"
                            >编辑
                            </el-button>
                            <el-button
                                    type="text"
                                    icon="el-icon-delete"
                                    class="danger"
                                    @click="handleDelete(scope.row)"
                            >删除
                            </el-button>
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
            <!--cpu-->
            <el-dialog title="告警规则" :visible.sync="ruleVisible" :show-close="false" width="65%" >
                <el-form :model="ruleValidateForm" style="margin-left: 50px" ref="ruleValidateForm" label-width="110px">
                    <el-form-item >
                        <el-row>
                            <el-col :span="12">
                                <el-form-item
                                        label="告警规则名称"
                                        prop="rule_name"
                                        :rules="[{ required: true, message: '名称不能为空'}]">
                                    <el-input v-model="ruleValidateForm.rule_name"></el-input>
                                </el-form-item>
                            </el-col>
                        </el-row>
                        <el-row class="mt10">
                            <el-col :span="6" class="mr10">
                                <el-select v-model="ruleValidateForm.alarm_object" placeholder="请选择监控类型" @change="clearServerOptions" :popper-append-to-body="false">
                                    <el-option value="服务器"></el-option>
                                    <el-option value="虚拟服务器"></el-option>
                                    <el-option value="中间件"></el-option>
                                    <el-option value="数据库"></el-option>
                                    <el-option value="防火墙"></el-option>
                                    <el-option value="路由器"></el-option>
                                    <el-option value="交换机"></el-option>
                                    <el-option value="负载均衡"></el-option>
                                    <el-option value="存储"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-select v-if="ruleValidateForm.alarm_object != '数据库' && ruleValidateForm.alarm_object !='中间件'" v-model="ruleValidateForm.tag_id" placeholder="请选择标签"  clearable @focus="get_tag()" @change="get_device" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in tagOptions"
                                            :key="item.id"
                                            :label="item.tag_name"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-select v-if="ruleValidateForm.alarm_object =='中间件'" v-model="ruleValidateForm.server_type" placeholder="请选择具体" @focus="get_middleware()" @change="clearIndex" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in middlewareOptions"
                                            :key="item.middleware_type"
                                            :label="item.middleware_type"
                                            :value="item.middleware_type">
                                    </el-option>
                                </el-select>
                                <el-select v-if="ruleValidateForm.alarm_object=='数据库'" v-model="ruleValidateForm.server_type" placeholder="请选择具体" @focus="get_db()" @change="clearIndex" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in dbOptions"
                                            :key="item.db_type"
                                            :label="item.db_type"
                                            :value="item.db_type">
                                    </el-option>
                                </el-select>
                                <el-select v-if="ruleValidateForm.alarm_object=='存储'" v-model="ruleValidateForm.server_type" placeholder="请选择具体" @focus="get_storage()" @change="clearIndex" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in storageOptions"
                                            :key="item.storage_type"
                                            :label="item.storage_type"
                                            :value="item.storage_type">
                                    </el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-select v-if="ruleValidateForm.alarm_object !='数据库' && ruleValidateForm.alarm_object !='中间件'" v-model="ruleValidateForm.business_id" placeholder="请选择业务" clearable @focus="get_business()" @change="get_device" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in businessOptions"
                                            :key="item.id"
                                            :label="item.name"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-col>
                        </el-row>
                        <el-row class="mt10">
                            <el-col :span="5" class="mr10">
                                <el-select v-model="ruleValidateForm.alarmIndex" placeholder="请选择监控项" @focus="get_index()" @change="ruleAddSelect" :popper-append-to-body="false">
                                    <el-option
                                            v-for="item in serverOptions"
                                            :key="item.indicator_name"
                                            :label="item.indicator"
                                            :disabled="item.disabled"
                                            :value="item.indicator_name + ' ' + item.indicator">
                                    </el-option>
                                </el-select>
                            </el-col>
                        </el-row>
                        <el-scrollbar v-if="ruleValidateForm.tag" style="height:100%;width: 95%"> <!-- 滚动条 -->
                            <!-- 注意需要给 el-scrollbar 设置高度，判断是否滚动是看它的height判断的 -->
                            <el-row  style="height: 120px;width: 100%;"><!--可显示区域-->
                                <el-table  :data="ruleValidateForm.tag">
                                    <el-table-column prop="device_ip" label="设备ip"></el-table-column>
                                    <el-table-column prop="device_name" label="设备名称" width="150"></el-table-column>
                                    <el-table-column prop="tag" label="标签" width="330"></el-table-column>
                                </el-table>
                            </el-row>
                        </el-scrollbar>
                    </el-form-item>
                    <el-form-item style="margin-left: 110px" class="mr20" v-show="showFlag==true">
                        <el-form  :rules="rules" ref="ruleDetailForm" v-if="ruleValidateForm.rule_detail" :model="ruleValidateForm.rule_detail[0]">
                            <el-form-item v-for="(domain,val) in ruleValidateForm.rule_detail" :key="domain.index">
                                <h4>{{domain.index_name}}</h4>
                                <el-form-item :span="24">
                                    <el-col :span="2">
                                        <span style="color: red">*</span>
                                        <span>策略</span>
                                    </el-col>
                                    <el-col :span="5">
                                        <el-select
                                                style="width:100%"
                                                class="cpu_div_sub"
                                                value-key="strategy_level"
                                                v-model="domain.alarm_strategy"
                                                placeholder="请选择策略"
                                                @focus="querystrategy()"
                                                :popper-append-to-body="false">
                                            <el-option v-for="item in strategyData"
                                                       :key="item.strategy_level"
                                                       :label="item.strategy_name"
                                                       :value="item.strategy_level">
                                            </el-option>
                                        </el-select>
                                    </el-col>
                                </el-form-item>
                                <el-form-item :span="24">
                                    <el-col class="cpu_ul" :span="18">
                                        <el-col :span="4">条件</el-col>
                                        <el-col :span="4">阈值</el-col>
                                        <el-col :span="5">轮询值</el-col>
                                        <el-col :span="4">
                                            <span style="color: red">*</span>
                                            等级
                                        </el-col>
                                        <el-col :span="5">通知方式</el-col>
                                        <el-col :span="3" class="el_col_bor_none"></el-col>
                                    </el-col>
                                    <el-button style="margin-right: 170px" type="danger" icon="el-icon-delete" @click="handleDel(domain.index,val)" circle plain  :span="2" ></el-button>
                                </el-form-item>
                                <el-form-item  v-for="(items,index) in domain.rule_num"
                                               :key="items.id"
                                               class="cpu_div">
                                    <el-col :span="3">
                                        <el-select v-model="items.operator" class="cpu_div_sub" :popper-append-to-body="false">
                                            <el-option value=">="></el-option>
                                            <el-option value="<="></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-input type="number" :min="minNum" v-model="items.threshold" class="cpu_threshold"></el-input>
                                        <span>{{
                                            domain.index=='cpu_percent' || domain.index=='mem_percent' ||
                                            domain.index=='disk_rate' || domain.index=='mem_fragmentation_ratio' ||
                                            domain.index=='heap' || domain.index=='nonheap' || domain.index=='rw_ratio' ||
                                            domain.index=='Processes_usage' || domain.index=='Session_usage' || domain.index=='HitRate' ?'%'
                                                :domain.index=='disk_read' || domain.index=='disk_write' || domain.index=='used_memory_peak' ?'字节/秒'
                                                :domain.index=='packets_recv' || domain.index=='packets_sent'?'数量'
                                                    :domain.index=='bytes_recv' || domain.index=='bytes_sent' ?'bps'
                                                        :ruleValidateForm.server_type=='WEBLOGIC' || ruleValidateForm.server_type=='RABBITMQ'
                                                        || domain.index=='connected_clients' || domain.index=='blocked_clients' ? '个': ''
                                            }}</span>
                                    </el-col>
                                    <el-col :span="3">
                                        <el-input type="number" :min="minNum" v-model="items.num" class="cpu_threshold"></el-input>
                                        <span>{{
                                            domain.alarm_strategy=='1' || domain.alarm_strategy=='2' ? '轮询'
                                                :domain.alarm_strategy=='3' || domain.alarm_strategy=='4' ? '分钟'
                                                :''
                                            }}
                                    </span>
                                    </el-col>
                                    <el-col :span="3">
                                        <el-select style="width:100%" class="cpu_div_sub" value-key="grade_level"  v-model="items.alarm_severity" placeholder="请选择" @focus="queryseverity()" :popper-append-to-body="false">
                                            <el-option v-for="item in severityData"
                                                       :key="item.grade_level"
                                                       :label="item.grade_name"
                                                       :value="item.grade_level">
                                            </el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="3">
                                        <el-select style="width:100%" class="cpu_div_sub" value-key="notification"  v-model="items.notification" placeholder="请选择" :popper-append-to-body="false">
                                            <el-option label="邮件" value="1"></el-option>
                                            <el-option label="短信" value="2"></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="3" class="mr_top8">
                                        <i  v-if="domain.rule_num.length==1"></i>
                                        <i class="el-icon-close" @click.prevent="removeDomain(val,index)" v-else-if="domain.rule_num.length!=1"></i>
                                    </el-col>
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                            @click="addCreateItem(val)"
                                            size="small"
                                            type="primary" plain
                                    >Add</el-button>
                                </el-form-item>
                            </el-form-item>
                        </el-form>
                    </el-form-item>
                    <el-form-item >
                        <el-row :gutter="20">
                            <el-col :span="6" :offset="18">
                                <el-button @click="resetCreate" class="change_el_button">取 消</el-button>
                                <el-button type="primary" @click="saveRuleCreate">确 定</el-button>
                            </el-col>
                        </el-row>
                    </el-form-item>
                </el-form>
            </el-dialog>
            <!-- 编辑弹出框 -->
            <el-dialog title="配置文件" :visible.sync="editVisible" :show-close="false" width="65%">
                <el-form :model="ruleEditForm" ref="ruleEditForm" label-width="110px">
                    <el-row class="mL40">
                        <el-col :span="12" :offset="2">
                            <el-form-item
                                    label="告警规则名称"
                                    prop="rule_name"
                                    :rules="[{ required: true, message: '名称不能为空'}]">
                                <el-input v-model="ruleEditForm.rule_name"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row class="mL40">
                        <el-col :span="4" :offset="2" class="mr10">
                            <el-input v-model="ruleEditForm.alarm_object" disabled></el-input>
                        </el-col>
                        <el-col :span="8" class="mr10">
                            <el-input v-model="ruleEditForm.tag" disabled></el-input>
                        </el-col>
                        <el-col :span="4" class="mr10" v-if="ruleEditForm.alarm_object=='数据库' || ruleEditForm.alarm_object=='中间件' || ruleEditForm.alarm_object === '存储'">
                            <el-input v-model="ruleEditForm.server_type" disabled></el-input>
                        </el-col>
                        <el-col :span="5">
                            <el-select v-model="ruleEditForm.alarmIndex" placeholder="请选择监控项" @focus="get_index1()" @change="ruleEditSelect" :popper-append-to-body="false">
                                <el-option
                                        v-for="item in serverOptions"
                                        :key="item.indicator_name"
                                        :label="item.indicator"
                                        :disabled="item.disabled"
                                        :value="item.indicator_name + ' ' + item.indicator">
                                </el-option>
                            </el-select>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="24" :offset="0">
                            <el-form-item v-for="(domain,val) in ruleEditForm.rule_detail" :key="domain.index">
                                <h4>{{domain.index_name}}</h4>
                                <el-row :span="20">
                                    <el-col :span="2">
                                        <span style="color: red">*</span>
                                        <label>策略</label></el-col>
                                    <el-col :span="5">
                                        <el-select class="cpu_div_sub" value-key="strategy_level"  v-model="domain.alarm_strategy" placeholder="请选择策略" @focus="querystrategy()" :popper-append-to-body="false">
                                            <el-option v-for="item in strategyData"
                                                       :key="item.strategy_level"
                                                       :label="item.strategy_name"
                                                       :value="item.strategy_level">
                                            </el-option>
                                        </el-select>
                                    </el-col>
                                </el-row>
                                <el-col class="cpu_ul" :span="18">
                                    <el-col :span="4">条件</el-col>
                                    <el-col :span="5">阈值</el-col>
                                    <el-col :span="5">轮询值</el-col>
                                    <el-col :span="5">
                                        <span style="color: red">*</span>
                                        等级</el-col>
                                    <el-col :span="3" class="el_col_bor_none"></el-col>
                                    <el-col :span="5">通知方式</el-col>
                                </el-col>
                                <el-button type="danger" icon="el-icon-delete" @click="handleDel1(domain.index,val)" circle plain  :span="2" ></el-button>
                                <el-form-item  v-for="(items,index) in domain.rule_num" :key="items.id" class="cpu_div">
                                    <el-col :span="3">
                                        <el-select v-model="items.operator" class="cpu_div_sub" :popper-append-to-body="false">
                                            <el-option value=">="></el-option>
                                            <el-option value="<="></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-input type="number" :min="minNum" v-model="items.threshold" class="cpu_threshold"></el-input>
                                        <span>{{
                                            domain.index=='cpu_percent' ?'%'
                                                :domain.index=='mem_percent' ?'%'
                                                :domain.index=='disk_rate' ?'%'
                                                    :domain.index=='disk_read' ?'字节/秒'
                                                        :domain.index=='disk_write' ?'字节/秒'
                                                            :domain.index=='packets_recv' ?'数量'
                                                                :domain.index=='packets_sent' ?'数量'
                                                                    :domain.index=='bytes_recv' ?'bps'
                                                                        :domain.index=='bytes_sent' ?'bps':''
                                            }}</span>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-input type="number" :min="minNum" v-model="items.num" class="cpu_threshold"></el-input>
                                        <span>{{
                                            domain.alarm_strategy=='1' ? '轮询'
                                                :domain.alarm_strategy=='2' ? '轮询'
                                                :domain.alarm_strategy=='3' ? '分钟'
                                                    :domain.alarm_strategy=='4' ? '分钟'
                                                        :''
                                            }}
                                    </span>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-select style="width:100%" class="cpu_div_sub" value-key="grade_name"
                                                   v-model="items.alarm_severity"
                                                   placeholder="请选择"
                                                   @focus="queryseverity()" :popper-append-to-body="false">
                                            <el-option v-for="item in severityData"
                                                       :key="item.grade_level"
                                                       :label="item.grade_name"
                                                       :value="item.grade_level">
                                            </el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-select style="width:100%" class="cpu_div_sub" value-key="notification"
                                                   v-model="items.notification"
                                                   placeholder="请选择"
                                                   :popper-append-to-body="false">
                                            <el-option label="邮件" value="1"></el-option>
                                            <el-option label="短信" value="2"></el-option>
                                        </el-select>
                                    </el-col>
                                    <el-col :span="3" class="mr_top8">
                                        <i  v-if="domain.rule_num.length==1"></i>
                                        <i class="el-icon-close" @click.prevent="removeEditDomain(val,index)" v-else-if="domain.rule_num.length!=1"></i>
                                    </el-col>
                                </el-form-item>
                                <el-form-item>
                                    <el-button
                                            @click="addEditItem(val)"
                                            size="small"
                                            type="primary" plain
                                    >Add</el-button>
                                </el-form-item>
                            </el-form-item>
                            <el-form-item >
                                <el-row :gutter="20">
                                    <el-col :span="6" :offset="18">
                                        <el-button @click="resetedit" class="change_el_button">取 消</el-button>
                                        <el-button type="primary" @click="saveEdit">确 定</el-button>
                                    </el-col>
                                </el-row>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
            </el-dialog>

        </div>
    </div>
</template>

<script>
    import ElFormItem from "../../../../node_modules/element-ui/packages/form/src/form-item";
    export default {
        components: {ElFormItem},
        name: 'alarmseverity',
        data() {
            return {
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                tableData: [],
                multipleSelection: [],
                delList: [],
                editVisible: false,
                pageTotal: 0,
                edit_form: {},
                form: {},
                idx: -1,
                id: -1,
                minNum: 1,
                searchData: {
                    rule_name: '',
                    alarm_object: '',
                    is_delete: 0,
                    device_name: '',
                    device_ip: ''
                },
                rules: {
                    alarm_strategy: [
                        {required: true, message: '请选择告警策略', trigger: 'blur'}
                    ],
                    alarm_level: [
                        {required: true, message: '请选择告警等级', trigger: 'blur'}
                    ]
                },
                objectData: [],
                indexData: [],
                strategyData: [],
                severityData: [],
                operatorData: [">=","<="],
                // notificationData: ['Phone', 'Message', 'Email'],
                ruleVisible: false,
                deviceVisible: false,
                serverOptions: [],
                dbOptions: [],
                middlewareOptions: [],
                storageOptions: [],
                tagOptions: [],
                businessOptions: [],
                deviceOptions: [],
                ruleValidateForm: {
                    rule_name: '',
                    alarm_object: '',
                    tag: '',
                    tag_id: "",
                    business_id: '',
                    server_type: '',
                    rule_detail: [
                        // {
                        // index:'',
                        // index_name: '',
                        // alarm_strategy:'',
                        // rule_num:[{
                        //     operator:'',
                        //     threshold:40,
                        //     num:'5',
                    //         alarm_severity:''
                    //     }]
                    // }
                    ],
                },
                ruleEditForm: {
                    rule_name: '',
                    alarm_object: "服务器",
                    rule_detail: [{
                        index: 'cpu_percent',
                        alarm_strategy: '1',
                        rule_num: [{
                            operator: '',
                            threshold: 40,
                            num: '5',
                            alarm_severity: '提示',
                            notification: '邮件'
                        }]
                    }],
                },
                ruleUnit: '%',
                showFlag: false,
                showTable: false,
                alarmStrategy:'',
                formdata: [1,2,3,4]
            };
        },
        created() {
            this.getData();
        },
        methods: {
            // 获取 easy-mock 的模拟数据
            getData() {
                this.$http.get(`monitor/api/alarm_rule/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&rule_name=${this.searchData.rule_name}&device_name=${
                    this.searchData.device_name}&device_ip=${this.searchData.device_ip}&is_delete=${this.searchData.is_delete}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.tableData = res.data.data;
                    this.pageTotal = res.data.total_count;
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 重置编辑
            resetedit() {
                this.editVisible = false;
                this.serverOptions = [];
            },
            //重置新增
            resetCreate() {
                this.ruleVisible = false;
                this.ruleValidateForm = {
                    rule_name: '',
                    alarm_object: '',
                    tag: '',
                    tag_id: "",
                    business_id: '',
                    server_type: '',
                    rule_detail: [
                    ],
                };
                this.serverOptions = [];
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning',
                    customClass: 'message-logout',
                    cancelButtonClass:'change_el_button'
                }).then(() => {
                    this.$http.put(`monitor/api/alarm_rule/${row.id}/logic_delete/`,
                        {'is_delete': 1},
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 200) {
                            this.$message.success('删除成功！');
                            this.$set(this.query, 'pageIndex', 1)
                            this.getData()
                        } else {
                            this.$message.error('删除失败！');
                            this.$set(this.query, 'pageIndex', 1)
                            this.getData()
                        }

                    }).catch((error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                })
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
            // 编辑操作
            handleEdit(row) {
                this.$http.get(`monitor/api/alarm_rule/${row.id}/get_one_rule/`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        },
                    }).then((res) => {
                    this.ruleEditForm = res.data;
                    for (let i in this.ruleEditForm.rule_detail) {
                        if (this.ruleEditForm.rule_detail[i].alarm_strategy == '1') {
                            this.ruleEditForm.rule_detail[i].alarm_strategy = '轮询次数'
                        } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '2') {
                            this.ruleEditForm.rule_detail[i].alarm_strategy = '轮询平均值'
                        } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '3') {
                            this.ruleEditForm.rule_detail[i].alarm_strategy = '持续时间'
                        } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '4') {
                            this.ruleEditForm.rule_detail[i].alarm_strategy = '平均时间'
                        }
                        for (let j in this.ruleEditForm.rule_detail[i].rule_num) {
                            if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '1') {
                                this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '提示'
                            } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '2') {
                                this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '报警'
                            } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '3') {
                                this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '重要'
                            } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '4') {
                                this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '严重'
                            } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '5'){
                                this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '紧急'
                            }
                        }
                    }
                    this.get_index1();
                    this.editVisible = true;
                })
            },
            // 保存编辑
            saveEdit() {
                if (this.ruleEditForm.rule_name === '') {
                    this.$message.warning('请输入告警规则名称')
                    return false
                }
                for (let k in this.ruleEditForm) {
                    if (k === 'rule_detail' && this.ruleEditForm[k].length === 0) {
                        this.$message.warning('请输入监控项')
                        return false
                    }
                    // if (this.ruleEditForm['rule_detail'].length === 0) {
                    //     this.$message.warning('请输入监控项')
                    //     return false
                    // }
                }
                for (let i in this.ruleEditForm['rule_detail']) {
                    if (this.ruleEditForm['rule_detail'][i]['alarm_strategy'] === '') {
                        this.$message.warning('请输入告警策略')
                        return false
                    }
                    for (let j in this.ruleEditForm['rule_detail'][i]['rule_num']) {
                        if (this.ruleEditForm['rule_detail'][i]['rule_num'][j]['alarm_severity'] === '') {
                            this.$message.warning('请输入告警等级')
                            return false
                        }
                    }
                }
                for (let i in this.ruleEditForm.rule_detail) {
                    if (this.ruleEditForm.rule_detail[i].alarm_strategy == '轮询次数') {
                        this.ruleEditForm.rule_detail[i].alarm_strategy = '1'
                    } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '轮询平均值') {
                        this.ruleEditForm.rule_detail[i].alarm_strategy = '2'
                    } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '持续时间') {
                        this.ruleEditForm.rule_detail[i].alarm_strategy = '3'
                    } else if (this.ruleEditForm.rule_detail[i].alarm_strategy == '平均时间') {
                        this.ruleEditForm.rule_detail[i].alarm_strategy = '4'
                    }
                    for (let j in this.ruleEditForm.rule_detail[i].rule_num) {
                        if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '提示') {
                            this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '1'
                        } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '报警') {
                            this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '2'
                        } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '重要') {
                            this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '3'
                        } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '严重') {
                            this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '4'
                        } else if (this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity == '紧急') {
                            this.ruleEditForm.rule_detail[i].rule_num[j].alarm_severity = '5'
                        }
                    }
                }
                this.$http.put(`monitor/api/alarm_rule/${this.ruleEditForm.id}/`,
                    {
                        'rule_name': this.ruleEditForm.rule_name, 'alarm_object': this.ruleEditForm.alarm_object,
                        'rule_detail': this.ruleEditForm.rule_detail
                    },
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                    if (res.status === 200) {
                        this.$message.success('修改成功！');
                        this.editVisible = false;
                        this.getData()
                    } else if (res.status === 205) {
                        this.$message.error("名称重复");
                        this.getData()
                    }
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            queryseverity() {
                this.$http.get(`monitor/api/alarm_severity/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.severityData = res.data;
                })
            },

            //查询业务信息
            querystrategy() {
                this.$http.get(`monitor/api/alarm_strategy/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    console.log(res)
                    this.strategyData = res.data
                })
            },
            //处理时间格式
            dateFormat(row, column) {
                const daterc = row[column.property]
                if (daterc != null) {
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
            settingFile() {
                this.ruleVisible = true;
            },
            //cpu
            removeDomain(val, index) {
                this.ruleValidateForm.rule_detail[val].rule_num.splice(index, 1);
            },
            removeEditDomain(val, index) {
                this.ruleEditForm.rule_detail[val].rule_num.splice(index, 1);
            },
            addCreateItem(val) {
                this.ruleValidateForm.rule_detail[val].rule_num.push({
                    operator: '>=',
                    threshold: 80,
                    num: '5',
                    alarm_severity: '',
                    notification: '邮件'
                })
            },
            addEditItem(val) {
                this.ruleEditForm.rule_detail[val].rule_num.push({
                    operator: '>=',
                    threshold: 80,
                    num: '5',
                    alarm_severity: '',
                    notification: '邮件'
                })
            },
            handleDel(domain, index) {
                this.ruleValidateForm.rule_detail.splice(index, 1);
                for (let i in this.serverOptions) {
                    if (this.serverOptions[i].indicator_name == domain) {
                        this.serverOptions[i].disabled = false;
                    }
                }
                this.ruleValidateForm.alarmIndex = '';
            },
            handleDel1(domain, index) {
                this.ruleEditForm.rule_detail.splice(index, 1);
                for (let i in this.serverOptions) {
                    if (this.serverOptions[i].indicator_name == domain) {
                        this.serverOptions[i].disabled = false;
                    }
                }
            },
            handleEditDel(domain, index) {
                this.ruleEditForm.rule_detail.splice(index, 1);
                for (let i in this.serverOptions) {
                    if (this.serverOptions[i].value == domain) {
                        this.serverOptions[i].disabled = false;
                    }
                }
            },

            get_tag() {
                this.$http.get(`monitor/api/tag/`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.tagOptions = res.data;
                    }
                )
            },
            get_business() {
                this.$http.get(`monitor/api/business/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.businessOptions = res.data;
                })
            },

            // 获取中间件监控类型
            get_middleware() {
                this.$http.get(`monitor/api/middleware/`,
                    {header: {
                            'token': localStorage.getItem('token')
                        }
                    }
                ).then((res) => {
                    this.middlewareOptions = res.data;

                })
            },

            // 获取数据库监控类型
            get_db() {
                this.$http.get(`monitor/api/databases/`,
                    {header: {
                            'token': localStorage.getItem('token')
                        }
                    }
                ).then((res) => {
                    this.dbOptions = res.data;
                })
            },

            // 获取存储监控类型
            get_storage() {
                this.$http.get(`monitor/api/storageitem/type`,
                    {
                        header: {
                            'token': localStorage.getItem('token')
                        }
                    }
                ).then((res) => {
                    this.storageOptions = res.data;
                })
            },

            // 获取监控指标
            get_index() {
                if (this.ruleValidateForm.alarm_object === '中间件' || this.ruleValidateForm.alarm_object === '数据库') {
                    if(this.serverOptions.length === 0) {
                        this.$http.get(`monitor/api/server_monitor/get_indicator/?specific_type=${this.ruleValidateForm.server_type}`, {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.serverOptions = res.data;
                            for (let i in this.serverOptions) {
                                this.serverOptions[i].disabled = false;
                            }
                        })
                    }
                } else if (this.ruleValidateForm.alarm_object === '服务器' || this.ruleValidateForm.alarm_object === '虚拟服务器') {
                    if(this.serverOptions.length === 0){
                        this.$http.get(`monitor/api/server_monitor/get_indicator/?monitor_type=server`, {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.serverOptions = res.data;
                            for (let i in this.serverOptions) {
                                this.serverOptions[i].disabled = false;
                            }
                        })
                    }
                // } else if (this.ruleValidateForm.alarm_object === '存储') {
                //     if(this.serverOptions.length === 0) {
                //         this.$http.get(`monitor/api/storageitem/storage/?storage_type=${this.ruleValidateForm.server_type}`,
                //             {
                //                 headers: {
                //                     'token': localStorage.getItem('token')
                //                 }
                //         }).then((res) => {
                //             this.serverOptions = res.data;
                //             console.log(this.serverOptions,111)
                //             console.log(res.data,111)
                //             for (let i in this.serverOptions) {
                //                 this.serverOptions[i].disabled = false;
                //                 this.serverOptions[i].indicator = this.serverOptions[i].item_name
                //                 this.serverOptions[i].indicator_name = this.serverOptions[i].item
                //
                //             }
                //         })
                //     }
                } else {
                    const new_tag = JSON.stringify(this.ruleValidateForm.tag)
                    if(this.serverOptions.length === 0) {
                        this.$http.get(`monitor/api/network_monitor/indicator/?device_type=${
                            this.ruleValidateForm.alarm_object}&tag=${new_tag}`, {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.serverOptions = res.data;
                            console.log(res.data,111)
                            for (let i in this.serverOptions) {
                                this.serverOptions[i].disabled = false;
                                this.serverOptions[i].indicator = this.serverOptions[i].indicator_name
                                this.serverOptions[i].indicator_name = this.serverOptions[i].indicator_code

                            }
                        })
                    }
                }
            },
            get_index1() {
                if (this.ruleEditForm.alarm_object === '中间件' || this.ruleEditForm.alarm_object === '数据库') {
                    this.$http.get(`monitor/api/server_monitor/get_indicator/?specific_type=${this.ruleEditForm.server_type}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.serverOptions = res.data;
                        for (let i in this.serverOptions) {
                            this.serverOptions[i].disabled = false;
                            for (let j in this.ruleEditForm.rule_detail) {
                                if (this.ruleEditForm.rule_detail[j].index == this.serverOptions[i].indicator_name) {
                                    this.serverOptions[i].disabled = true;
                                }
                            }
                        }
                    })
                } else if (this.ruleEditForm.alarm_object === '服务器' || this.ruleEditForm.alarm_object === '虚拟服务器') {
                    if(this.serverOptions.length === 0) {
                        this.$http.get(`monitor/api/server_monitor/get_indicator/?monitor_type=server`, {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            this.serverOptions = res.data;
                            for (let i in this.serverOptions) {
                                this.serverOptions[i].disabled = false;
                                for (let j in this.ruleEditForm.rule_detail) {
                                    if (this.ruleEditForm.rule_detail[j].index == this.serverOptions[i].indicator_name) {
                                        this.serverOptions[i].disabled = true;
                                    }
                                }
                            }
                        })
                    }
                } else if (this.ruleEditForm.alarm_object === '存储') {
                    this.$http.get(`monitor/api/storageitem/storage/?storage_type=${this.ruleEditForm.server_type}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.serverOptions = res.data;
                        for (let i in this.serverOptions) {
                            this.serverOptions[i].disabled = false;
                            this.serverOptions[i].indicator = this.serverOptions[i].item_name
                            this.serverOptions[i].indicator_name = this.serverOptions[i].item
                            for (let j in this.ruleEditForm.rule_detail) {
                                if (this.ruleEditForm.rule_detail[j].index == this.serverOptions[i].indicator_name) {
                                    this.serverOptions[i].disabled = true;
                                }
                            }
                        }
                    })
                } else {
                    this.$http.get(`monitor/api/network_monitor/indicator/?device_type=${this.ruleEditForm.alarm_object}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.serverOptions = res.data;
                        for (let i in this.serverOptions) {
                            this.serverOptions[i].disabled = false;
                            this.serverOptions[i].indicator = this.serverOptions[i].indicator_name
                            this.serverOptions[i].indicator_name = this.serverOptions[i].indicator_code
                            for (let j in this.ruleEditForm.rule_detail) {
                                if (this.ruleEditForm.rule_detail[j].index == this.serverOptions[i].indicator_name) {
                                    this.serverOptions[i].disabled = true;
                                }
                            }
                        }
                    })
                }
            },
            clearServerOptions() {
              this.serverOptions = [];
              this.ruleValidateForm.tag_id = '';
              this.ruleValidateForm.business_id = '';
              this.ruleValidateForm.server_type='';
              this.ruleValidateForm.alarmIndex = '';
              this.ruleValidateForm.rule_detail = [];
              this.get_device();
            },
            clearIndex() {
                this.get_device();
                this.serverOptions = [];
                this.ruleValidateForm.rule_detail = [];
                this.ruleValidateForm.alarmIndex = '';
            },
            ruleAddSelect() {
                this.showFlag = true;
                console.log(this.ruleValidateForm.alarmIndex.split(" ")[0], 1111)
                for (let i in this.serverOptions) {
                    if (this.serverOptions[i].indicator_name == this.ruleValidateForm.alarmIndex.split(" ")[0]) {
                        this.serverOptions[i].disabled = true;
                    }
                }
                this.ruleValidateForm.rule_detail.push({
                    index: this.ruleValidateForm.alarmIndex.split(' ')[0],
                    index_name: this.ruleValidateForm.alarmIndex.split(' ')[1],
                    alarm_strategy: '',
                    rule_num: [{
                        operator: '>=',
                        threshold: '30',
                        num: '3',
                        alarm_severity: '',
                        notification: '邮件'
                    }]
                });
            },
            ruleEditSelect() {
                for (let i in this.serverOptions) {
                    if (this.serverOptions[i].indicator_name == this.ruleEditForm.alarmIndex.split(' ')[0]) {
                        this.serverOptions[i].disabled = true;
                    }
                }
                this.ruleEditForm.rule_detail.push({
                    index: this.ruleEditForm.alarmIndex.split(' ')[0],
                    index_name: this.ruleEditForm.alarmIndex.split(' ')[1],
                    alarm_strategy: '',
                    rule_num: [{
                        operator: '>=',
                        threshold: 30,
                        num: '3',
                        alarm_severity: '',
                        notification: '邮件'
                    }]
                });
                this.ruleEditForm.alarmIndex = '';
            },

            get_device() {
                if (this.ruleValidateForm.alarm_object === '数据库') {
                    this.$http.get(`monitor/api/databases/tag/?server_type=${
                        this.ruleValidateForm.server_type}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.ruleValidateForm.tag = res.data;
                        this.deviceVisible = true;
                    })
                } else if (this.ruleValidateForm.alarm_object === '中间件') {
                    this.$http.get(`monitor/api/middleware/tag/?server_type=${
                        this.ruleValidateForm.server_type}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.ruleValidateForm.tag = res.data;
                        this.deviceVisible = true;
                    })
                } else {
                    this.$http.get(`monitor/api/device/device_info/?device_type=${
                        this.ruleValidateForm.alarm_object}&tag_id=${this.ruleValidateForm.tag_id}&business_id=${
                        this.ruleValidateForm.business_id}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        this.ruleValidateForm.tag = res.data;
                        this.deviceVisible = true;
                    })
                }

            },
            saveRuleCreate() {
                for (let k in this.ruleValidateForm) {
                    if (k === 'rule_detail' && this.ruleValidateForm[k].length === 0) {
                        this.$message.warning('请输入监控项')
                        return false
                    }
                }
                for (let i in this.ruleValidateForm['rule_detail']) {
                    if (this.ruleValidateForm['rule_detail'][i]['alarm_strategy'] === '') {
                        this.$message.warning('请输入告警策略')
                        return false
                    }
                    for (let j in this.ruleValidateForm['rule_detail'][i]['rule_num']) {
                        if (this.ruleValidateForm['rule_detail'][i]['rule_num'][j]['alarm_severity'] === '') {
                            this.$message.warning('请输入告警等级')
                            return false
                        }
                    }
                }
                this.$refs.ruleValidateForm.validate((valid) => {
                    if (valid) {
                        delete this.ruleValidateForm.alarmIndex;
                        // this.get_device()
                        this.$http.post(`monitor/api/alarm_rule/`,
                            this.ruleValidateForm,
                            {
                                headers: {
                                    'token': localStorage.getItem('token')
                                }
                            }).then((res) => {
                            if (res.status === 201) {
                                this.$message.success('创建成功！');
                                this.getData();
                            } else {
                                this.$message.error('创建失败！');
                            }
                            this.ruleVisible = false;
                            this.serverOptions = [];
                            this.ruleValidateForm = {};
                        })
                    } else {
                        // this.$message.error('创建失败！');
                        this.$message.warning('请输入告警规则名称');
                        return false;
                    }
                });
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    @import "../../../assets/scss/darkStyle";
    .handle-box {
        margin-bottom: 20px;
    }
    .handle-select {
        width: 120px;
    }
    .handle-input {
        width: 180px;
        display: inline-block;
    }

    .table {
        width: 100%;
        font-size: 14px;
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
    /*cpu*/
    .cpu_ul{
        margin: 0 8px;
        text-align: center;
        /deep/ .el-col{
            border-bottom: 1px solid #c0ccda;
        }
        .el_col_bor_none{
            border: none;
        }

    }
    .cpu_div{
        text-align: center;
        margin-top: 5px;
        .cpu_div_sub{
            width: 95%;
        }
        .cpu_threshold{
            width: 60%;
        }
    }
    /deep/ .el-form-item--small.el-form-item{
        margin-bottom: 5px;
    }
    .mt10{
        margin-top:10px;
    }
    .mr20{
        margin-left:25px;
        /deep/ .el-form-item__content{
            margin-left: 0!important;
        }
    }
    .mL40{
        margin-left:40px;
    }
</style>
<style>
    .message-logout{
        background-color:#24273e;
        border: 1px solid #3c4163;
        color:#fff;
    }
    .el-message-box__title{
        color:#409EFF;
    }
    .el-message-box__content{
        color:#fff;
    }
    .change_el_button{
        background: #2a2e49;
        border: 1px solid #2f3561;
        color:#fff;
    }
</style>
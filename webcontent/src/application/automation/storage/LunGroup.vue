<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> LUN
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
                                    class="selectIp" @change="changeQueryHost">
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
                <el-tab-pane label="LUN" name="1">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <el-col :span="17">
                            <div>
                                <el-button
                                        type="primary"
                                        @click="handleAdd()"
                                        class="handle-box"
                                >创建
                                </el-button>
                            </div>
                        </el-col>
                        <el-col :span="2">
                            <el-select v-model="SearchName">
                                <el-option label="名称" value="name"></el-option>
                                <el-option label="ID" value="id"></el-option>
                                <el-option label="健康状态" value="health"></el-option>
                                <el-option label="运行状态" value="running"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="3" class="mr10">
                            <el-input v-model="nameSearch" v-if="SearchName==='name'" placeholder="关键字"></el-input>
                            <el-input v-model="idSearch" v-if="SearchName==='id'" placeholder="关键字"></el-input>
                            <el-select v-if="SearchName==='health'" v-model="healthSelect">
                                <el-option label="全部" value="all"></el-option>
                                <el-option label="正常" value="1"></el-option>
                                <el-option label="故障" value="2"></el-option>
                            </el-select>
                            <el-select v-if="SearchName==='running'" v-model="runningSelect">
                                <el-option label="全部" value="all"></el-option>
                                <el-option label="在线" value="27"></el-option>
                                <el-option label="离线" value="28"></el-option>
                                <el-option label="初始化中" value="53"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="2">
                            <el-button size="small" @click="queryLun">搜索</el-button>
                        </el-col>
                    </el-row>
                    <el-table
                        v-loading="lunloading"
                        element-loading-text="拼命加载中"
                        element-loading-spinner="el-icon-loading"
                        :data="tableData"
                        border
                        style="width: 100%"
                    >
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                        <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                        <af-table-column prop="ALLOCTYPE" label="类型" align="center" :formatter="handlealloctype"></af-table-column>
                        <af-table-column prop="USAGETYPE" label="使用类型" align="center" :formatter="handleusagetype"></af-table-column>
                        <af-table-column prop="CAPACITY" label="容量" align="center" :formatter="handlecapacity"></af-table-column>
                        <af-table-column prop="PARENTNAME" label="所属存储池" align="center"></af-table-column>
                        <af-table-column prop="EXPOSEDTOINITIATOR" label="映射状态" align="center" :formatter="handleexposedtoinitiator"></af-table-column>
                    </el-table>
                </el-tab-pane>
                <el-tab-pane label="LUN组" name="2">
                    <el-row type="flex" class="row-bg" justify="space-between">
                        <el-col :span="17">
                            <div>
                                <el-button
                                        type="primary"
                                        @click="handleAddlungroup()"
                                        class="handle-box"
                                >创建
                                </el-button>
                            </div>
                        </el-col>
                        <el-col :span="2">
                            <el-select v-model="lungroupSearchName">
                                <el-option label="名称" value="name"></el-option>
                                <el-option label="ID" value="id"></el-option>
                            </el-select>
                        </el-col>
                        <el-col :span="3" class="mr10">
                            <el-input v-model="lungroupnameSearch" v-if="lungroupSearchName==='name'" placeholder="关键字"></el-input>
                            <el-input v-model="lungroupidSearch" v-if="lungroupSearchName==='id'" placeholder="关键字"></el-input>
                        </el-col>
                        <el-col :span="2">
                            <el-button size="small" @click="queryLunGroup">搜索</el-button>
                        </el-col>
                    </el-row>
                    <el-table
                            v-loading="lunloading"
                            element-loading-text="拼命加载中"
                            element-loading-spinner="el-icon-loading"
                            :data="lungrouptableData"
                            border
                            style="width: 100%"
                            highlight-current-row
                            @row-click="selectlungroup"
                    >
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                        <af-table-column prop="CAPCITY" label="LUN总容量" align="center" :formatter="handleluncapacity"></af-table-column>
                    </el-table>
                        <el-col>
                            <span>选择LUN组查看对应LUN信息:</span>
                        </el-col>
                        <el-col>
                            <el-table
                                    :data="luntableData"
                                    border
                                    style="width: 100%"
                            >
                                <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                                <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                                <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                                <af-table-column prop="ALLOCTYPE" label="类型" align="center" :formatter="handlealloctype"></af-table-column>
                                <af-table-column prop="CAPACITY" label="容量" align="center" :formatter="handlecapacity"></af-table-column>
                                <af-table-column prop="PARENTNAME" label="所属存储池" align="center"></af-table-column>
                                <af-table-column prop="EXPOSEDTOINITIATOR" label="映射状态" align="center" :formatter="handleexposedtoinitiator"></af-table-column>
                                <af-table-column prop="WWN" label="WWN" align="center"></af-table-column>
                            </el-table>
                        </el-col>
                </el-tab-pane>
            </el-tabs>
        </div>
        <el-dialog title="创建LUN" :visible.sync="addlunVisible" width="32%">
            <el-form ref="lunform" :rules="lunrules" :model="lunform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="lunform.NAME"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="lunform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-form-item label="起始ID" :required="idrequired">
                    <el-row>
                        <el-col :span="18">
                            <el-input v-model="lunform.ID" id='ID' class="create-input" :disabled="iddisabled"></el-input>
                        </el-col>
                        <el-col :span="6">
                            <el-checkbox v-model="idchecked" @change="handleID">自动分配</el-checkbox>
                        </el-col>
                    </el-row>
                </el-form-item>
                <el-form-item label="使用类型">
                    <el-select v-model="LUNUSAGETYPE" @change="selectusagetype($event)">
                        <el-option
                                v-for="item in usagetypeOptions"
                                :key="item.value"
                                :label="item.label"
                                :value="item.value">
                        </el-option>
                    </el-select>
                </el-form-item>
                <el-form-item label="SmartThin" v-if="smartthinshow">
                    <el-row>
                        <el-checkbox v-model="smartthinchecked" @change="handlesmartthin">启用</el-checkbox>
                    </el-row>
                    <el-row class="span-height">
                        <span>启用SmartThin功能后，存储系统将创建thin LUN，且不会一次性分配已设置的容量给该LUN。在该LUN容量范围内，存储系统会根据主机实际使用的容量动态分配存储资源，实现按需分配。</span>
                    </el-row>
                </el-form-item>
                <el-form-item label="所属存储池">
                    <el-row>
                        <el-select v-model="LUNPARENTID" @change="getcapacity($event)">
                            <el-option
                                    v-for="item in parentidOptions"
                                    :key="item.NAME"
                                    :label="item.NAME"
                                    :value="item">
                            </el-option>
                        </el-select>
                    </el-row>
                    <el-row class="span-height">
                        <span>可用容量{{totalcapacity}}</span>
                    </el-row>
                </el-form-item>
                <el-form ref="capacityform" :rules="capacityrules" :model="capacityform" label-width="85px">
                    <el-form-item label="容量" prop="CAPACITY" v-if="capacityshow">
                        <el-row>
                            <el-col :span="18">
                                <el-input type="number" v-model="capacityform.CAPACITY"  class="create-input" @input="handleaddlun"></el-input>
                            </el-col>
                            <el-col :span="6">
                                <el-select v-model="capacityunit" @change="handlecapacityunit">
                                    <el-option
                                            v-for="item in capacityOptions"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-col>
                        </el-row>
                    </el-form-item>
                </el-form>
                <el-form-item label="数量" prop="luncount">
                    <el-row>
                       <el-input v-model="luncount" type="number" class="create-input" @input="handeluncount"></el-input>
                    </el-row>
                    <el-row class="span-height">
                        <span>每次最多可创建500个LUN。当创建多个LUN时，系统会根据数量自动在输入的名称后增加后缀编号以示区分。您也可以手动指定后缀编号。</span>
                    </el-row>
                    <el-row>
                        <el-checkbox v-model="luncountchecked" :disabled="luncountdisabled" @change="handlestartunit">手动指定后缀编号</el-checkbox>
                    </el-row>
                    <el-row>
                        <el-col :span="16">
                            <el-form-item label="起始编号" v-if="startnumbershow" prop="startnumber">
                                <el-input v-model="startnumber" type="number" @input="handlestartnumber"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="6">
                            <span v-if="startnumbershow">(0~{{10000-luncount}})</span>
                        </el-col>
                    </el-row>
                </el-form-item>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addlunVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveAddLunList" :disabled="savelunDisabled">确 定</el-button>
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

        <el-dialog title="创建LUN组" :visible.sync="addgrouplunVisible" width="77%">
            <el-form ref="lungroupform" :rules="lungrouprules" :model="lungroupform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="lungroupform.NAME"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="lungroupform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-row>
                    <el-col :span="11">
                        <p class="lungroup_create_p">可选LUN</p>
                        <el-row type="flex" class="row-bg margin_bot" justify="end">
                            <el-col :span="6">
                                <el-select v-model="leftSearchName">
                                    <el-option label="名称" value="name"></el-option>
                                    <el-option label="ID" value="id"></el-option>
                                    <el-option label="健康状态" value="health"></el-option>
                                    <el-option label="运行状态" value="running"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-input v-model="leftnameSearch" v-if="leftSearchName==='name'" placeholder="关键字"></el-input>
                                <el-input v-model="leftidSearch" v-if="leftSearchName==='id'" placeholder="关键字"></el-input>
                                <el-select v-if="leftSearchName==='health'" v-model="lefthealthSelect">
                                    <el-option label="全部" value="all"></el-option>
                                    <el-option label="正常" value="1"></el-option>
                                    <el-option label="故障" value="2"></el-option>
                                </el-select>
                                <el-select v-if="leftSearchName==='running'" v-model="leftrunningSelect">
                                    <el-option label="全部" value="all"></el-option>
                                    <el-option label="在线" value="27"></el-option>
                                    <el-option label="离线" value="28"></el-option>
                                    <el-option label="初始化中" value="53"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="3">
                                <el-button size="small" @click="queryleftLun">搜索</el-button>
                            </el-col>
                        </el-row>
                        <div class="div-height">
                        <el-table
                                ref="lunTable"
                                :key="tableKey"
                                :row-key="getRowKeys"
                                :data="nogrouptableData"
                                border
                                fit
                                highlight-current-row
                                @selection-change="handlelungroupChange"
                                class="margin_bot"
                        >
                            <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                            <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                            <af-table-column prop="PARENTNAME" label="所属存储池" align="center"></af-table-column>
                            <af-table-column prop="CAPACITY" label="容量" align="center" :formatter="handlecapacity"></af-table-column>
                            <af-table-column prop="ISADD2LUNGROUP" label="已归属LUN组" align="center" :formatter="handleisadd2lungroup"></af-table-column>
                        </el-table>
                        </div>
                        <el-checkbox label="仅显示未归属于LUN组的LUN" v-model="LUNchecked" @change="handlegetLun"></el-checkbox>
                    </el-col>
                    <el-col :span="2" class="trans_create_but">
                        <el-button
                                @click="addlun"
                                type="primary"
                                :disabled="!lungroupData.length"
                                icon="el-icon-arrow-right"
                                circle
                        ></el-button>
                        <br>
                        <el-button
                                @click="removelun"
                                type="primary"
                                :disabled="!selectedLunList.length"
                                icon="el-icon-arrow-left"
                                circle
                                style="margin-left: 0;margin-top: 10px;"
                        ></el-button>
                    </el-col>
                    <el-col :span="11">
                        <p class="lungroup_create_p">已选LUN</p>
                        <el-row type="flex" class="row-bg margin_bot" justify="end">
                            <el-col :span="6">
                                <el-select v-model="rightSearchName">
                                    <el-option label="名称" value="name"></el-option>
                                    <el-option label="ID" value="id"></el-option>
                                    <el-option label="健康状态" value="health"></el-option>
                                    <el-option label="运行状态" value="running"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="6" class="mr10">
                                <el-input v-model="rightnameSearch" v-if="rightSearchName==='name'" placeholder="关键字"></el-input>
                                <el-input v-model="rightidSearch" v-if="rightSearchName==='id'" placeholder="关键字"></el-input>
                                <el-select v-if="rightSearchName==='health'" v-model="righthealthSelect">
                                    <el-option label="全部" value="all"></el-option>
                                    <el-option label="正常" value="1"></el-option>
                                    <el-option label="故障" value="2"></el-option>
                                </el-select>
                                <el-select v-if="rightSearchName==='running'" v-model="rightrunningSelect">
                                    <el-option label="全部" value="all"></el-option>
                                    <el-option label="在线" value="27"></el-option>
                                    <el-option label="离线" value="28"></el-option>
                                    <el-option label="初始化中" value="53"></el-option>
                                </el-select>
                            </el-col>
                            <el-col :span="3">
                                <el-button size="small" @click="queryrightLun">搜索</el-button>
                            </el-col>
                        </el-row>
                        <div class="div-height">
                        <el-table
                                ref="selectedlunTable"
                                :key="tableKey"
                                :row-key="getRowKeys"
                                :data="selectedLuntableData"
                                border
                                fit
                                highlight-current-row
                                @selection-change="handleSelectedLunChange"
                        >
                            <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                            <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                            <af-table-column prop="PARENTNAME" label="所属存储池" align="center"></af-table-column>
                            <af-table-column prop="CAPACITY" label="容量" align="center" :formatter="handlecapacity"></af-table-column>
                            <af-table-column prop="ISADD2LUNGROUP" label="已归属LUN组" align="center" :formatter="handleisadd2lungroup"></af-table-column>
                        </el-table>
                        </div>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addgrouplunVisible = false">取 消</el-button>
                <el-button type="primary" @click="createlungroup">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="执行结果" :visible.sync="addlungroupresultVisible" width="30%">
            <el-table
                    :data="lungroupresultData"
                    border
                    style="width: 100%"
            >
                <af-table-column prop="name" label="操作" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="reason" label="失败原因和建议" align="center"></af-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addlungroupresult">关闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "LunGroup",
        data() {
            return {
                storageresult: {}, // 查询的存储的数据
                storage_env: '',
                activeIndex: '1', // 默认在lun页面
                tableData: [], // 查询一条存储返回的数据
                copytableData: [],
                storageHost: '',  // 存储搜索框默认显示的值
                addlunVisible: false, // 创建时弹框的设置
                lunform: {}, // 创建时传的参数
                LUNTYPE: 0, // 获得当前id时的type
                lunrules: {
                    NAME: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ],
                    ID: [{ message: '请输入ID', trigger: 'input'}]
                },
                capacityform: {},
                capacityrules: {
                    CAPACITY: [
                        {required: true, message: '请输入容量'},
                        {trigger: 'blur'}
                    ],
                },
                hostData: [],  // 实时查询存储获取的数据
                idchecked: true,  //默认id自动分配为选中状态
                iddisabled: true, // 默认id输入禁用
                idrequired: false,  // 默认id不需要
                usagetypeOptions: [
                    {
                        label: "普通LUN",
                        value: '0'
                    },
                    {
                        label: 'PE LUN',
                        value: '3'
                    }
                ],
                smartthinchecked: false, // smartthin 未选中状态
                parentidOptions: [], //存储池的查询数据
                totalcapacity: 0,  // 存储池的总容量
                lunloading: false,  // 查询lun的列表时加载
                addlunloading: false,
                capacitychecked: false,  // 全部容量为未选中状态
                capacityOptions: [
                    {
                        value: 'KB'
                    },
                    {
                        value: 'MB'
                    },
                    {
                        value: 'GB'
                    },
                    {
                        value: 'TB'
                    }
                ], // 容量单位的选择
                capacityunit: 'GB', // 容量单位默认是GB
                luncountchecked: false, //lun数量默认不选
                luncountdisabled: true, // lun数量后缀默认不可选
                luncount: 1, // lun数量默认是1
                smartthinshow: true, // 默认smartthin是展示的
                capacityshow: true,
                startnumber: 0,
                startnumbershow: false, // 起始编号默认不展示
                LUNUSAGETYPE: '普通LUN',
                LUNPARENTID: '',
                addresultVisible: false,
                CAPACITY: '',
                resultData:[],  //创建lun的执行结果
                lungrouptableData: [],  // lungroup的查询结果
                addgrouplunVisible: false, // 创建lun组弹框默认不提示
                lungrouprules: {
                    NAME: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ],
                },
                lungroupform: {},
                tree_title: ['可选LUN', '已选LUN'],
                fromDataTree: [],
                ISADD2LUNGROUP: '',
                nogrouptableData: [],
                selectedLunList: [],
                tableKey: 0,
                lungroupData: [],
                selectedLuntableData: [],
                lungroupresultData:[],  //创建lun组的执行结果
                addlungroupresultVisible: false,
                lunGroupSearchName:'name',
                lunGroupSearchValue:'',
                SearchName: 'name',
                healthSelect: '全部',
                runningSelect: '全部',
                nameSearch: '',
                idSearch: '',
                lungroupSearchName: 'name',
                lungroupnameSearch: '',
                lungroupidSearch: '',
                copylungrouptableData: [],
                luntableData: [],
                savelunDisabled: true,
                LUNchecked: true,
                leftSearchName: 'name',
                leftnameSearch: '',
                leftidSearch: '',
                copynogrouptableData: [],
                lefthealthSelect: '全部',
                leftrunningSelect: '全部',
                copyselectedLuntableData: [],
                rightSearchName: 'name',
                rightnameSearch: '',
                rightidSearch: '',
                righthealthSelect: '全部',
                rightrunningSelect: '全部',
                totalcapacitysectors: 0
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getLunList(){
                this.lunloading = true
                this.$http.post( `automation/api/storage/lun_list/?ISADD2LUNGROUP=${this.ISADD2LUNGROUP}`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data['data'];
                    this.copytableData = this.tableData
                    this.lunloading = false
                    this.nogrouptableData = this.tableData
                    this.copynogrouptableData = this.tableData
                    for (let i = 0; i < this.copyselectedLuntableData.length; i++) {
                        for (let j = 0; j < this.nogrouptableData.length; j++) {
                            if (
                                this.copyselectedLuntableData[i] &&
                                this.nogrouptableData[j] &&
                                this.copyselectedLuntableData[i].NAME === this.nogrouptableData[j].NAME
                            ) {
                                this.nogrouptableData.splice(j, 1);
                            }
                        }
                    }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data.msg))
                    this.lunloading = false
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
                            this.storageresult = this.storage_env;
                            this.getLunList();
                            this.storageHost = this.storage_env['hostname'] + '/' + this.storage_env['manage_ip'];
                        }else{
                            this.$message.error('未发现存储环境!')
                        }
                }).catch( (error) => {
                    console.log(error, 9999)
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            //处理健康状态
            handlehealthstatus(row){
                return row.HEALTHSTATUS == '1' ? '正常' : row.HEALTHSTATUS == '2' ? '故障': '';
            },
            //处理运行状态
            handlerunningstatus(row){
                return row.RUNNINGSTATUS == '53' ? '初始化中': row.RUNNINGSTATUS == '27'? '在线' : row.RUNNINGSTATUS == '28' ? '离线': row.RUNNINGSTATUS == '19' ? '正在格式化': '';
            },
            // 处理空间分配类型
            handlealloctype(row){
                return row.ALLOCTYPE == '0' ? 'thick LUN' : row.ALLOCTYPE == '1' ? 'thin LUN': '';
            },
            //处理使用类型
            handleusagetype(row){
                return row.USAGETYPE == '0' ? '内部': row.USAGETYPE == '1' ? '外部' : row.USAGETYPE == '3'?'PE LUN': '';
            },
            //处理容量
            handlecapacity(row){
                let capacity
                capacity = row.CAPACITY
                let capacity_mb = capacity*512/1024/1024
                let capacity_gb = capacity_mb/1024
                if(capacity_gb >= 1){
                    capacity_gb = capacity_gb.toString().substring(0,capacity_gb.toString().indexOf(".")+4)
                    capacity_gb = parseFloat(capacity_gb).toFixed(3)
                    return capacity_gb + ' GB'
                }else{
                    return parseFloat(capacity_mb).toFixed(3) + ' MB'
                }
            },
            // 处理lungroup的容量
            handleluncapacity(row){
                let capacity
                capacity = row.CAPCITY
                let capacity_mb = capacity*512/1024/1024
                let capacity_gb = capacity_mb/1024
                if(capacity_gb >= 1){
                    capacity_gb = capacity_gb.toString().substring(0,capacity_gb.toString().indexOf(".")+4)
                    capacity_gb = parseFloat(capacity_gb).toFixed(3)
                    return capacity_gb + ' GB'
                }else{
                    return parseFloat(capacity_mb).toFixed(3) + ' MB'
                }
            },
            //处理是否映射
            handleexposedtoinitiator(row){
                return row.EXPOSEDTOINITIATOR == 'false' ? '未映射' : row.EXPOSEDTOINITIATOR == 'true' ? '已映射' : '未映射';
            },
            handleAdd(){
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                this.lunform = {}
                // this.CAPACITY = ''
                this.capacityform = {}
                this.capacityunit = 'GB'
                this.$set(this.lunform, 'USAGETYPE', '0')
                this.$set(this.lunform, 'ALLOCTYPE', 0)
                this.$set(this.lunform, 'WRITEPOLICY', 1)
                this.idchecked = true
                this.iddisabled = true
                this.luncount = 1
                this.luncountchecked = false
                this.luncountdisabled = true
                this.startnumbershow = false
                this.startnumber = 0
                this.smartthinshow = true
                this.capacityshow = true
                this.copyselectedLuntableData = []
                // 查询availidid
                this.$http.post( `automation/api/storage/nextavailableid/?type=11`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let avaliableid = res['data']['ID']
                    avaliableid = parseInt(avaliableid) +1
                    let id_len = avaliableid.toString().length
                    if(id_len===1){
                        this.$set(this.lunform, 'NAME', 'LUN00'+avaliableid)
                    }else if(id_len===2){
                        this.$set(this.lunform, 'NAME', 'LUN0'+avaliableid)
                    }else{
                        this.$set(this.lunform, 'NAME', 'LUN'+avaliableid)
                    }
                    // 查询存储池
                    this.$http.post( `automation/api/storage/storagepool_list/`, {'manage_address': this.storageresult.manage_address,
                        'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                        headers:{
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.parentidOptions = res['data']
                        this.LUNPARENTID = this.parentidOptions[0].NAME
                        this.getcapacity(this.parentidOptions[0])
                        this.lunform.PARENTID = this.parentidOptions[0]
                        loading.close();
                        this.addlunVisible = true;
                        this.$nextTick(()=>{
                            this.$refs.lunform.clearValidate();
                            this.$refs.capacityform.clearValidate();
                        })
                    }).catch( (error) => {
                        loading.close();
                        this.$message.error(JSON.stringify(error.response.data.msg))
                    });
                }).catch( (error) => {
                    loading.close();
                    this.$message.error(JSON.stringify(error.response.data.msg))
                });
            },
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
            // 改变存储ip时查询lun的信息
            changeQueryHost(row){
                console.log(row, 44444)
                sessionStorage.setItem('storage_env', JSON.stringify(row));
                this.storageresult = row;
                this.storageHost = row.hostname + '/' + row.manage_ip
                this.lungrouptableData = []
                this.tableData = []
                this.luntableData = []
                if(this.activeIndex==='1'){
                    this.getLunList()
                }else{
                    this.getlungroupList()
                }
            },
            // 处理id输入不输入的问题
            handleID(){
                this.iddisabled = !this.iddisabled
                this.idrequired = !this.idrequired
                if(this.iddisabled){
                    this.$set(this.lunform, 'ID', '')  //清空输入的id值
                }
            },
            getcapacity(res){
                console.log(res.DATASPACE, 'DATASPACE')
                let capacity= res.DATASPACE
                this.totalcapacitysectors = capacity
                let capacity_mb = capacity*512/1024/1024
                let capacity_gb = capacity_mb/1024
                if(capacity_gb >= 1){
                    capacity_gb = capacity_gb.toString().substring(0,capacity_gb.toString().indexOf(".")+4)
                    capacity_gb = parseFloat(capacity_gb).toFixed(3)
                    this.totalcapacity = capacity_gb + ' GB'
                }else{
                    this.totalcapacity = parseFloat(capacity_mb).toFixed(3) + ' MB'
                }
                console.log(this.totalcapacity, 'totalcapacity')
                this.$set(this.lunform, 'PARENTID', this.LUNPARENTID)
            },
            // 选择使用类型时判断smartthin和容量是否隐藏
            selectusagetype(res){
                if(res==='3'){
                    this.smartthinshow = false
                    this.capacityshow = false
                    this.savelunDisabled = false
                    this.$set(this.lunform, 'WRITEPOLICY', 2)
                    this.$set(this.lunform, 'PARENTTYPE', 216)
                    this.$set(this.lunform, 'SUBTYPE', 2)
                }else{
                    this.smartthinshow = true
                    this.capacityshow = true
                    this.$set(this.lunform, 'WRITEPOLICY', 1)
                }
                this.$set(this.lunform, 'USAGETYPE', parseInt(this.LUNUSAGETYPE))
            },
            // 处理数量大于1的情况
            handeluncount(res){
                if(res<='1'){
                    this.luncountdisabled = true
                }else{
                    this.luncountdisabled = false
                }
            },
            //处理起始编号
            handlestartunit(){
                this.startnumbershow = !this.startnumbershow
            },
            //处理启用的问题
            handlesmartthin(){
                if(this.smartthinchecked){
                    this.$set(this.lunform, 'ALLOCTYPE', 1)
                }else{
                    this.$set(this.lunform, 'ALLOCTYPE', 0)
                }
            },
            saveAddLunList(){
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
                this.addresultVisible = true
                this.$set(this.lunform, 'PARENTID', this.lunform.PARENTID.ID)
                this.LUNUSAGETYPE = '普通LUN'
                // let capacity = this.CAPACITY
                let capacity = this.capacityform.CAPACITY
                if(capacity){
                    if(this.capacityunit==='KB'){
                        this.$set(this.lunform, 'CAPACITY', capacity*1024/512)
                    }else if(this.capacityunit==='MB'){
                        this.$set(this.lunform, 'CAPACITY', capacity*1024*1024/512)
                    }else if(this.capacityunit==='GB'){
                        this.$set(this.lunform, 'CAPACITY', capacity*1024*1024*1024/512)
                    }else{
                        this.$set(this.lunform, 'CAPACITY', capacity*1024*1024*1024*1024/512)
                    }
                }
                this.$set(this.lunform, 'manage_address', this.storageresult.manage_address)
                this.$set(this.lunform, 'manage_username', this.storageresult.manage_username)
                this.$set(this.lunform, 'manage_password', this.storageresult.manage_password)
                if(this.luncount===1){
                    this.resultData = []
                    let add_res = {'name': this.lunform.NAME, 'status': '正在执行', 'reason': '', 'real_name': this.lunform.NAME}
                    this.resultData.push(add_res)
                    this.saveAddLun(add_res)
                }else{
                    if(this.resultData.length!=0){
                        CustomForeach(this.resultData, async (e) => {
                            await this.saveAddLun(e);
                    })}else{
                        for (var i=0;i<this.luncount;i++)
                        {
                            let id_len = i.toString().length
                            let name = ''
                            let real_name = ''
                            if(id_len===1){
                                real_name = this.lunform.NAME + '000' + i
                                name = "创建LUN " + real_name
                            }else if(id_len===2){
                                real_name = this.lunform.NAME + '00' + i
                                name = "创建LUN " + real_name
                            }else if(id_len===3) {
                                real_name = this.lunform.NAME + '0' + i
                                name = "创建LUN " + real_name
                            }else{
                                real_name = this.lunform.NAME + i
                                name = "创建LUN " + real_name
                            }
                            this.resultData.push({'name': name, 'status': '等待执行', 'reason': '', 'real_name': real_name})
                        }
                        CustomForeach(this.resultData, async (e) => {
                            await this.saveAddLun(e);

                        });
                    }
                }
            },
            saveAddLun(add_res){
                return new Promise((resolve, reject) => {
                    this.lunform.NAME = add_res.real_name
                    add_res.status = '正在执行'
                    this.$http.post(`automation/api/storage/create_lun/`, this.lunform, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        if(res.status===200){
                            add_res.status = '成功'
                        }
                        resolve(res)
                        console.log(resolve, reject, 'resolve')
                    }).catch( (error)=> {
                        reject(error)
                        add_res.status = '执行失败'
                        add_res.reason = error.response.data.msg
                        this.$message.error(JSON.stringify(error.response.data.msg));
                    });
                })

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
            //执行结果点击关闭时
            addresult(){
                this.addresultVisible = false
                this.addlunVisible = false
                this.getLunList()
            },
            handleStepOPtions(tab){
                if(tab.name==='1'){
                    this.ISADD2LUNGROUP = ''
                    this.getLunList(this.storageresult)
                }else{
                    this.luntableData = []
                    this.getlungroupList()
                }
            },
            //查询lungroup
            getlungroupList(){
                this.lunloading = true
                this.$http.post( `automation/api/storage/lun_group_list/`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.lungrouptableData = res.data['data'];
                    this.copylungrouptableData = this.lungrouptableData
                    this.lunloading = false
                }).catch( (error) => {
                    this.lunloading = false
                    this.$message.error(JSON.stringify(error.response.data.msg))
                });
            },
            handleAddlungroup(){
                this.lungroupform = {}
                this.selectedLuntableData = []
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                this.ISADD2LUNGROUP = false
                // 查询availidid
                this.$http.post( `automation/api/storage/nextavailableid/?type=256`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_passwords},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let avaliableid = res['data']['ID']
                    avaliableid = parseInt(avaliableid) +1
                    let id_len = avaliableid.toString().length
                    if(id_len===1){
                        this.$set(this.lungroupform, 'NAME', 'LUNGroup00'+avaliableid)
                    }else if(id_len===2){
                        this.$set(this.lungroupform, 'NAME', 'LUNGroup0'+avaliableid)
                    }else{
                        this.$set(this.lungroupform, 'NAME', 'LUNGroup'+avaliableid)
                    }
                    loading.close();
                    this.addgrouplunVisible = true;
                    this.$nextTick(()=>{
                        this.$refs.lungroupform.clearValidate();
                    })
                }).catch( (error) => {
                    loading.close();
                    this.$message.error(JSON.stringify(error.response.data.msg))
                });
                this.getLunList()
            },
            handlelungroupChange(rows){
                this.lungroupData = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.lungroupData.push(row);
                        }
                    });
                }
            },
            // 左边表格选择项移到右边
            addlun() {
                setTimeout(() => {
                    this.$refs["lunTable"].clearSelection();
                    this.$refs["selectedlunTable"].clearSelection();
                }, 0);
                this.lungroupData.forEach(item => {
                    this.selectedLuntableData.push(item);
                });
                this.copyselectedLuntableData = this.selectedLuntableData
                for (let i = this.nogrouptableData.length-1; i >= 0; i--) {
                    for (let j = 0; j < this.lungroupData.length; j++) {
                        if (
                            this.nogrouptableData[i] &&
                            this.lungroupData[j] &&
                            this.nogrouptableData[i].NAME === this.lungroupData[j].NAME
                        ) {
                            this.nogrouptableData.splice(i, 1);
                        }
                    }
                }
            },
            // 右边表格选择项移到左边
            removelun() {
                setTimeout(() => {
                    this.$refs["lunTable"].clearSelection();
                    this.$refs["selectedlunTable"].clearSelection();
                }, 0);
                this.selectedLunList.forEach(item => {
                    this.nogrouptableData.push(item);
                });
                for (let i = this.selectedLuntableData.length-1; i >= 0; i--) {
                    for (let j = 0; j < this.selectedLunList.length; j++) {
                        if (
                            this.selectedLuntableData[i] &&
                            this.selectedLunList[j] &&
                            this.selectedLuntableData[i].NAME === this.selectedLunList[j].NAME
                        ) {
                            this.selectedLuntableData.splice(i, 1);
                        }
                    }
                }
            },
            // 将右边表格选择项存入selectedStaffData中
            handleSelectedLunChange(rows){
                this.selectedLunList = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.selectedLunList.push(row);
                        }
                    });
                }
            },
            //处理是否归属lun组
            handleisadd2lungroup(row){
                return row.ISADD2LUNGROUP == 'false' ? '否' : row.ISADD2LUNGROUP == 'true' ? '是':"";
            },
            getRowKeys(row) {
                return row.NAME;
            },
            // 创建lungroup并添加lun
            createlungroup(){
                this.lungroupresultData = []
                let name = "创建LUN组 " + this.lungroupform.NAME
                let add_res = {'name': name, 'status': '正在执行', 'reason': ''}
                this.lungroupresultData.push(add_res)
                for (var i=0;i<this.selectedLuntableData.length;i++)
                {
                    let lun_name = "增加LUN " + this.selectedLuntableData[i].NAME
                    this.lungroupresultData.push({'name': lun_name, 'status': '等待执行', 'reason': '','lun_id': this.selectedLuntableData[i].ID})
                }
                this.addlungroupresultVisible = true
                this.create_lun_group()
            },
            create_lun_group(){
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
                this.$http.post(`automation/api/storage/create_lun_group/`, {'lun_group': this.lungroupform,
                    'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                'manage_address': this.storageresult.manage_address}, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        let lun_group_data = res.data
                    if(res.status===200){
                        this.lungroupresultData[0].status = '成功'
                    }else{
                        this.lungroupresultData[0].status = '执行失败'
                        this.lungroupresultData[0].reason = res.data
                    }
                    if(lun_group_data){
                        CustomForeach(this.lungroupresultData, async (e, i) => {
                            if(i>0){
                                await this.lungroupassociate(e, lun_group_data.ID);
                            }
                        });
                    }
                })
            },
            // lungroup添加lun
            lungroupassociate(add_res, group_id){
                return new Promise((resolve, reject) => {
                    this.lungroupform.NAME = add_res.real_name
                    add_res.status = '正在执行'
                    this.$http.post(`automation/api/storage/lun_group_associate/`, {
                        'lun_associate':{'ID': group_id, "ASSOCIATEOBJTYPE": 11, "ASSOCIATEOBJID": add_res.lun_id}, 'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                        'manage_address': this.storageresult.manage_address
                    }, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        if(res.status===200){
                            add_res.status = '成功'
                        }else{
                            add_res.status = '执行失败'
                            add_res.reason = res.data
                        }
                        resolve(res)
                        console.log(resolve, reject, 'resolve')
                    }).catch( (error)=> {
                        reject(error)
                        add_res.status = '执行失败'
                        add_res.reason = error.response.data.msg
                        this.$message.error(JSON.stringify(error.response.data.msg));
                    });
                })
            },
            addlungroupresult(){
                this.addlungroupresultVisible = false
                this.addgrouplunVisible = false
                this.getlungroupList()
            },
            queryLun(){
                if(this.SearchName==='name'){
                    if(this.nameSearch!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.nameSearch);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }else if(this.SearchName==='id'){
                    if(this.idSearch!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.idSearch);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }else if(this.SearchName==='health'){
                    if(this.healthSelect==='全部'|| this.healthSelect==='all'){
                        this.tableData = this.copytableData
                    }else{
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.HEALTHSTATUS.includes(this.healthSelect);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }
                }else if(this.SearchName==='running') {
                    if (this.runningSelect === '全部' || this.runningSelect === 'all') {
                        this.tableData = this.copytableData
                    } else {
                        this.tableData = []
                        this.copytableData.forEach((item) => {
                            let incledes_res = item.RUNNINGSTATUS.includes(this.runningSelect);
                            if (incledes_res === true) {
                                this.tableData.push(item)
                            }
                        })
                    }
                }
            },
            queryLunGroup(){
                console.log(this.lungroupSearchName, 1111)
                if(this.lungroupSearchName==='name'){
                    if(this.lungroupnameSearch!=''){
                        this.lungrouptableData = []
                        this.copylungrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.lungroupnameSearch);
                            if(incledes_res===true){
                                this.lungrouptableData.push(item)
                            }
                        })
                    }else{
                        this.lungrouptableData = this.copylungrouptableData
                    }
                }else if(this.lungroupSearchName==='id'){
                    if(this.lungroupidSearch!=''){
                        this.lungrouptableData = []
                        this.copylungrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.lungroupidSearch);
                            if(incledes_res===true){
                                this.lungrouptableData.push(item)
                            }
                        })
                    }else{
                        this.lungrouptableData = this.copylungrouptableData
                    }
                }
            },
            selectlungroup(row) {
                this.luntableData = []
                this.$http.post(`automation/api/storage/associate_group/?TYPE=11&ASSOCIATEOBJTYPE=${row.TYPE}&ASSOCIATEOBJID=${row.ID}`, {
                    'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username,
                    'manage_password': this.storageresult.manage_password
                }, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.luntableData = res.data
                }).catch((error) => {
                    this.$message.error(JSON.stringify(error.response.data.msg))
                    this.luntableData = []
                });
            },
            handleaddlun(){
                let capacity = 0
                if(this.capacityunit==='KB'){
                    capacity = this.capacityform.CAPACITY*1024/512
                }else if(this.capacityunit==='MB'){
                    capacity = this.capacityform.CAPACITY*1024*1024/512
                }else if(this.capacityunit==='GB'){
                    capacity = this.capacityform.CAPACITY*1024*1024*1024/512
                    console.log(capacity)
                }else{
                    capacity = this.capacityform.CAPACITY*1024*1024*1024*1024/512
                }
                if(parseInt(capacity) > parseInt(this.totalcapacitysectors)){
                    this.$message.error('存储池的可用容量小于创建LUN所需总容量，请重新选择存储池或修改LUN的总容量')
                    this.savelunDisabled = true
                }else{
                    if(this.LUNUSAGETYPE==='3'){
                        if(this.lunform.NAME&&this.luncount){
                            this.savelunDisabled = false
                        }
                    }else{
                        if(this.lunform.NAME&&this.capacityform.CAPACITY&&this.luncount){
                            this.savelunDisabled = false
                        }
                    }
                }
            },
            handlecapacityunit(){
                let capacity = 0
                if(this.capacityunit==='KB'){
                    capacity = this.capacityform.CAPACITY*1024/512
                }else if(this.capacityunit==='MB'){
                    capacity = this.capacityform.CAPACITY*1024*1024/512
                }else if(this.capacityunit==='GB'){
                    capacity = this.capacityform.CAPACITY*1024*1024*1024/512
                    console.log(capacity)
                }else{
                    capacity = this.capacityform.CAPACITY*1024*1024*1024*1024/512
                }
                if(parseInt(capacity) > parseInt(this.totalcapacitysectors)){
                    this.$message.error('存储池的可用容量小于创建LUN所需总容量，请重新选择存储池或修改LUN的总容量')
                    this.savelunDisabled = true
                }else{
                    this.savelunDisabled = false
                }
            },
            handlegetLun(){
                if(this.LUNchecked===true){
                    this.ISADD2LUNGROUP = false
                    this.getLunList()
                }else{
                    this.ISADD2LUNGROUP = ''
                    this.getLunList()
                }
            },
            queryleftLun(){
                if(this.leftSearchName==='name'){
                    if(this.leftnameSearch!=''){
                        this.nogrouptableData = []
                        this.copynogrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.leftnameSearch);
                            if(incledes_res===true){
                                this.nogrouptableData.push(item)
                            }
                        })
                    }else{
                        this.nogrouptableData = this.copynogrouptableData
                    }
                }else if(this.leftSearchName==='id'){
                    if(this.leftidSearch!=''){
                        this.nogrouptableData = []
                        this.copynogrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.leftidSearch);
                            if(incledes_res===true){
                                this.nogrouptableData.push(item)
                            }
                        })
                    }else{
                        this.nogrouptableData = this.copynogrouptableData
                    }
                }else if(this.leftSearchName==='health'){
                    if(this.lefthealthSelect==='全部'|| this.lefthealthSelect==='all'){
                        this.nogrouptableData = this.copynogrouptableData
                    }else{
                        this.nogrouptableData = []
                        this.copynogrouptableData.forEach((item)=>{
                            let incledes_res = item.HEALTHSTATUS.includes(this.lefthealthSelect);
                            if(incledes_res===true){
                                this.nogrouptableData.push(item)
                            }
                        })
                    }
                }else if(this.leftSearchName==='running') {
                    if (this.leftrunningSelect === '全部' || this.leftrunningSelect === 'all') {
                        this.nogrouptableData = this.copynogrouptableData
                    } else {
                        this.nogrouptableData = []
                        this.copynogrouptableData.forEach((item) => {
                            let incledes_res = item.RUNNINGSTATUS.includes(this.leftrunningSelect);
                            if (incledes_res === true) {
                                this.nogrouptableData.push(item)
                            }
                        })
                    }
                }
            },
            queryrightLun(){
                if(this.rightSearchName==='name'){
                    if(this.rightnameSearch!=''){
                        this.selectedLuntableData = []
                        this.copyselectedLuntableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.rightnameSearch);
                            if(incledes_res===true){
                                this.selectedLuntableData.push(item)
                            }
                        })
                    }else{
                        this.selectedLuntableData = this.copyselectedLuntableData
                    }
                }else if(this.rightSearchName==='id'){
                    if(this.rightidSearch!=''){
                        this.selectedLuntableData = []
                        this.copyselectedLuntableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.rightidSearch);
                            if(incledes_res===true){
                                this.selectedLuntableData.push(item)
                            }
                        })
                    }else{
                        this.selectedLuntableData = this.copyselectedLuntableData
                    }
                }else if(this.rightSearchName==='health'){
                    if(this.righthealthSelect==='全部'|| this.righthealthSelect==='all'){
                        this.selectedLuntableData = this.copyselectedLuntableData
                    }else{
                        this.selectedLuntableData = []
                        this.copyselectedLuntableData.forEach((item)=>{
                            let incledes_res = item.HEALTHSTATUS.includes(this.righthealthSelect);
                            if(incledes_res===true){
                                this.selectedLuntableData.push(item)
                            }
                        })
                    }
                }else if(this.rightSearchName==='running') {
                    if (this.rightrunningSelect === '全部' || this.rightrunningSelect === 'all') {
                        this.selectedLuntableData = this.copyselectedLuntableData
                    } else {
                        this.selectedLuntableData = []
                        this.copyselectedLuntableData.forEach((item) => {
                            let incledes_res = item.RUNNINGSTATUS.includes(this.rightrunningSelect);
                            if (incledes_res === true) {
                                this.selectedLuntableData.push(item)
                            }
                        })
                    }
                }
            },


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
.lungroup_create_p{
    border-bottom: 1px solid #C0C4CC;
    padding-bottom: 6px;
    margin-bottom: 10px;
}
    .trans_create_but{
        text-align: center;
        margin-top: 10%;
    }
    .div-height{
        height: 280px;
        overflow: auto;
    }
    .span-height{
        font-size: 10px;
        line-height: 22px;
    }
</style>

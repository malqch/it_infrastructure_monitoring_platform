<template>
    <div>
       <!-- <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> LUN
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>-->
        <div class="container">
            <el-form red="form">
                <el-row>
                    <el-col :span="17">
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
                    </el-col>
                </el-row>
            </el-form>
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
                    <el-select v-model="mappingviewSearchName">
                        <el-option label="名称" value="name"></el-option>
                        <el-option label="ID" value="id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="3">
                    <el-input v-model="nameSearchValue" v-if="mappingviewSearchName==='name'" placeholder="关键字"></el-input>
                    <el-input v-model="idSearchValue" v-if="mappingviewSearchName==='id'" placeholder="关键字"></el-input>
                </el-col>
                <el-col :span="2">
                    <el-button size="small" @click="querymappingview">搜索</el-button>
                </el-col>
            </el-row>
            <el-table
                    v-loading="mappingviewloading"
                    element-loading-text="拼命加载中"
                    element-loading-spinner="el-icon-loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    highlight-current-row
                    @row-click="selectmapping"
            >
                <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                <af-table-column prop="ID" label="ID" align="center"></af-table-column>
            </el-table>
            <el-row>
                <el-tabs v-model="activeIndex" @tab-click="handleStepOPtions">
                    <el-tab-pane label="LUN组" name="1">
                        <span>LUN组: {{groupname}}</span>
                        <el-table
                                :data="grouptableData"
                                border
                                style="width: 100%"
                        >
                            <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                            <af-table-column prop="ASSOCIATEMETADATA" label="主机LUN ID" align="center" :formatter="handlehostlunid"></af-table-column>
                            <af-table-column prop="ALLOCTYPE" label="类型" align="center" :formatter="handlealloctype"></af-table-column>
                            <af-table-column prop="USAGETYPE" label="使用类型" align="center" :formatter="handleusagetype"></af-table-column>
                            <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                            <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlelunrunningstatus"></af-table-column>
                            <af-table-column prop="CAPACITY" label="容量" align="center" :formatter="handlecapacity"></af-table-column>
                            <af-table-column prop="PARENTNAME" label="所属存储池" align="center"></af-table-column>
                            <af-table-column prop="WWN" label="WWN" align="center"></af-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="主机组" name="2">
                        <span>主机组: {{groupname}}</span>
                        <el-table
                                :data="grouptableData"
                                border
                                style="width: 100%"
                        >
                            <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                            <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                            <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                            <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlehostrunningstatus"></af-table-column>
                            <af-table-column prop="OPERATIONSYSTEM" label="操作系统" align="center" :formatter="handleoperationsystem"></af-table-column>
                            <af-table-column prop="IP" label="IP地址" align="center"></af-table-column>
                            <af-table-column prop="INITIATORNUM" label="启动器数量" align="center"></af-table-column>
                        </el-table>
                    </el-tab-pane>
                    <el-tab-pane label="端口组" name="3">
                        <span>端口组: {{groupname}}</span>
                        <el-table
                                :data="grouptableData"
                                border
                                style="width: 100%"
                        >
                            <af-table-column prop="TYPE" label="类型" align="center" :formatter="handletype"></af-table-column>
                            <af-table-column prop="LOCATION" label="位置" align="center"></af-table-column>
                            <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                            <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                        </el-table>
                    </el-tab-pane>
                </el-tabs>
            </el-row>
        </div>
        <el-dialog title="创建映射视图" :visible.sync="addmappingVisible" width="30%">
            <el-form ref="mappingviewform" :rules="mappingviewrules" :model="mappingviewform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="mappingviewform.NAME"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="mappingviewform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-form-item label="LUN组" prop="lungroupname">
                    <el-row>
                        <el-col :span="17">
                            <el-input v-model="lungroupname" class="create-input"  :disabled="true"></el-input>
                        </el-col>
                        <el-col :span="7">
                            <el-button size="small" plain @click="checklungroup" :loading="lungrouploading">选择</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
                <el-form-item label="主机组" prop="hostgroupname">
                    <el-row>
                        <el-col :span="17">
                            <el-input v-model="hostgroupname" class="create-input"  :disabled="true"></el-input>
                        </el-col>
                        <el-col :span="7">
                            <el-button size="small" plain @click="checkhostgroup" :loading="hostgrouploading">选择</el-button>
                        </el-col>
                    </el-row>
                </el-form-item>
                <el-checkbox v-model="portGroupChecked" class="portcheck" @change="selectPortGroupChecked">
                    <el-form-item label="端口组">
                        <el-row>
                            <el-col :span="16">
                                <el-input v-model="portgroupname" :disabled="true"></el-input>
                            </el-col>
                            <el-col :span="4">
                                <el-button size="small" plain :disabled="portGroupDisabled" @click="checkportgroup" :loading="portgrouploading">选择</el-button>
                            </el-col>
                            <el-col :span="4">
                                <el-button size="small" plain :disabled="portGroupDisabled" @click="Addport()">创建</el-button>
                            </el-col>
                        </el-row>
                    </el-form-item>
                </el-checkbox>

            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addmappingVisible = false">取 消</el-button>
                <el-button type="primary" :disabled="dangerTipDisabled" @click="dangerTip">确 定</el-button>
            </span>
        </el-dialog>

        <el-dialog title="选择LUN组" :visible.sync="selectlungroupVisible" width="30%">
            <el-row type="flex" class="row-bg margin_bot" justify="end">
                <el-col :span="4">
                    <el-select v-model="lungroupSearch">
                        <el-option label="名称" value="name"></el-option>
                        <el-option label="ID" value="id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="8" class="mr10">
                    <el-input v-model="namelungroupValue" v-if="lungroupSearch==='name'" placeholder="关键字"></el-input>
                    <el-input v-model="idlungroupValue" v-if="lungroupSearch==='id'" placeholder="关键字"></el-input>
                </el-col>
                <el-col :span="3">
                    <el-button size="small" @click="querylungroup">搜索</el-button>
                </el-col>
            </el-row>
            <el-row>
                <div class="div-height">
                    <el-table
                            :data="lungrouptableData"
                            border
                            highlight-current-row
                            style="width: 100%"
                            @row-click="selectlungroup"
                    >
                        <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                        <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                        <af-table-column prop="ISADD2MAPPINGVIEW" label="已归属映射视图" align="center" :formatter="handleISADD2MAPPINGVIEW"></af-table-column>
                    </el-table>
                </div>
            </el-row>
            <el-row style="margin-top: 30px;">
                <el-checkbox v-model="lungroupchecked" @change="handlelungroup">仅显示未归属于映射视图的LUN组</el-checkbox>
            </el-row>
            <el-row style="margin-top: 15px;">
                <el-checkbox v-model="lunidchecked" @change="handlelungroup">设置主机LUN ID</el-checkbox>
            </el-row>
            <el-row>
                <el-form>
                    <el-col :span="6">
                        <el-form-item label="起始ID: " v-if="lunidchecked" label-width="85px">
                            <el-input v-model="startid" class="create-input" @input="handlestartid"></el-input>
                        </el-form-item>
                    </el-col>
                </el-form>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="selectlungroupVisible = false">取 消</el-button>
                <el-button type="primary" :disabled="addlungroupDisabled" @click="addlungroup">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="选择主机组" :visible.sync="selecthostgroupVisible" width="30%">
            <el-row type="flex" class="row-bg margin_bot" justify="end">
                <el-col :span="4">
                    <el-select v-model="hostgroupSearch">
                        <el-option label="名称" value="name"></el-option>
                        <el-option label="ID" value="id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="8" class="mr10">
                    <el-input v-model="namehostgroupValue" v-if="hostgroupSearch==='name'" placeholder="关键字"></el-input>
                    <el-input v-model="idhostgroupValue" v-if="hostgroupSearch==='id'" placeholder="关键字"></el-input>
                </el-col>
                <el-col :span="3">
                    <el-button size="small" @click="queryhostgroup">搜索</el-button>
                </el-col>
            </el-row>
            <el-row>
                <el-table
                        :data="hostgrouptableData"
                        border
                        highlight-current-row
                        style="width: 100%"
                        @row-click="selecthostgroup"
                >
                    <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                    <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                </el-table>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="selecthostgroupVisible = false">取 消</el-button>
                <el-button type="primary" @click="addhostgroup" :disabled="addhostgroupDisabled">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="选择端口组" :visible.sync="selectportgroupVisible" width="30%">
            <el-row type="flex" class="row-bg margin_bot" justify="end">
                <el-col :span="4">
                    <el-select v-model="portgroupSearch">
                        <el-option label="名称" value="name"></el-option>
                        <el-option label="ID" value="id"></el-option>
                    </el-select>
                </el-col>
                <el-col :span="8" class="mr10">
                    <el-input v-model="nameportgroupValue" v-if="portgroupSearch==='name'" placeholder="关键字"></el-input>
                    <el-input v-model="idportgroupValue" v-if="portgroupSearch==='id'" placeholder="关键字"></el-input>
                </el-col>
                <el-col :span="3">
                    <el-button size="small" @click="queryportgroup">搜索</el-button>
                </el-col>
            </el-row>
            <el-row>
                <el-table
                        :data="portgrouptableData"
                        border
                        highlight-current-row
                        style="width: 100%"
                        @row-click="selectportgroup"
                >
                    <af-table-column prop="NAME" label="名称" align="center"></af-table-column>
                    <af-table-column prop="ID" label="ID" align="center"></af-table-column>
                </el-table>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="selectportgroupVisible = false">取 消</el-button>
                <el-button type="primary" :disabled="selectportgroupDisabled" @click="addpostgroup">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="创建端口组" :visible.sync="addportgroupVisible" width="77%">
            <el-form ref="portroupform" :rules="portrouprules" :model="portgroupform" label-width="85px">
                <el-form-item label="名称" prop="NAME">
                    <el-input v-model="portgroupform.NAME"></el-input>
                </el-form-item>
                <el-form-item label="描述">
                    <el-input type="textarea" v-model="portgroupform.DESCRIPTION"></el-input>
                </el-form-item>
                <el-row>
                        <el-col :span="11">
                            <p class="portgroup_create_p">可选端口</p>
                            <el-row type="flex" class="row-bg margin_bot" justify="end">
                                <el-col :span="6">
                                    <el-select v-model="portGroupSearchName">
                                        <el-option label="位置" value="location"></el-option>
                                        <el-option label="类型" value="type"></el-option>
                                        <el-option label="健康状态" value="health"></el-option>
                                        <el-option label="运行状态" value="running"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="6" class="mr10">
                                    <el-input v-model="portGroupSearchValue" v-if="portGroupSearchName==='location'" placeholder="关键字"></el-input>
                                    <el-select v-if="portGroupSearchName==='type'" v-model="typeSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="FC端口" value='212'></el-option>
                                        <el-option label="以太网端口" value='213'></el-option>
                                        <el-option label="FCoE端口" value='252'></el-option>
                                        <el-option label="IB端口" value='16500'></el-option>
                                    </el-select>
                                    <el-select v-if="portGroupSearchName==='health'" v-model="healthSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="正常" value="1"></el-option>
                                        <el-option label="故障" value="2"></el-option>
                                    </el-select>
                                    <el-select v-if="portGroupSearchName==='running'" v-model="runningSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="正常" value="1"></el-option>
                                        <el-option label="运行" value="2"></el-option>
                                        <el-option label="已连接" value="10"></el-option>
                                        <el-option label="未连接" value="11"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="3">
                                    <el-button size="small" @click="queryleftportData">搜索</el-button>
                                </el-col>
                            </el-row>
                            <div class="div-height">
                            <el-table
                                    ref="portTable"
                                    :key="tableKey"
                                    :row-key="getRowKeys"
                                    :data="leftPortTableData"
                                    border
                                    fit
                                    highlight-current-row
                                    @selection-change="handleportgroupChange"
                                    class="margin_bot"
                            >
                                <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                                <af-table-column prop="TYPE" label="类型" align="center" :formatter="handletype"></af-table-column>
                                <af-table-column prop="LOCATION" label="位置" align="center"></af-table-column>
                                <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                                <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                            </el-table>
                            </div>
                        </el-col>
                        <el-col :span="2" class="trans_create_but">
                            <el-button
                                    @click="addporttoright"
                                    type="primary"
                                    :disabled="!leftportData.length"
                                    icon="el-icon-arrow-right"
                                    circle
                            ></el-button>
                            <br>
                            <el-button
                                    @click="removeporttoleft"
                                    type="primary"
                                    :disabled="!selectedportList.length"
                                    icon="el-icon-arrow-left"
                                    circle
                                    style="margin-left: 0;margin-top: 10px;"
                            ></el-button>
                        </el-col>
                        <el-col :span="11">
                            <p class="portgroup_create_p">已选端口</p>
                            <el-row type="flex" class="row-bg margin_bot" justify="end">
                                <el-col :span="6">
                                    <el-select v-model="portrightSearchName">
                                        <el-option label="位置" value="location"></el-option>
                                        <el-option label="类型" value="type"></el-option>
                                        <el-option label="健康状态" value="health"></el-option>
                                        <el-option label="运行状态" value="running"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="6" class="mr10">
                                    <el-input v-model="rightLocationValue" v-if="portrightSearchName==='location'" placeholder="关键字"></el-input>
                                    <el-select v-if="portrightSearchName==='type'" v-model="righttypeSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="FC端口" value='212'></el-option>
                                        <el-option label="以太网端口" value='213'></el-option>
                                        <el-option label="FCoE端口" value='252'></el-option>
                                        <el-option label="IB端口" value='16500'></el-option>
                                    </el-select>
                                    <el-select v-if="portrightSearchName==='health'" v-model="righthealthSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="正常" value="1"></el-option>
                                        <el-option label="故障" value="2"></el-option>
                                    </el-select>
                                    <el-select v-if="portrightSearchName==='running'" v-model="rightrunningSelect">
                                        <el-option label="全部" value="all"></el-option>
                                        <el-option label="正常" value="1"></el-option>
                                        <el-option label="运行" value="2"></el-option>
                                        <el-option label="已连接" value="10"></el-option>
                                        <el-option label="未连接" value="11"></el-option>
                                    </el-select>
                                </el-col>
                                <el-col :span="3">
                                    <el-button size="small" @click="queryrightportData">搜索</el-button>
                                </el-col>
                            </el-row>
                            <div class="div-height">
                                <el-table
                                        ref="selectedportTable"
                                        :key="tableKey"
                                        :row-key="getRowKeys"
                                        :data="selectedPorttableData"
                                        border
                                        fit
                                        highlight-current-row
                                        @selection-change="handleSelectedPortChange"
                                >
                                    <el-table-column type="selection" :reserve-selection="true" width="55"></el-table-column>
                                    <af-table-column prop="TYPE" label="类型" align="center" :formatter="handletype"></af-table-column>
                                    <af-table-column prop="LOCATION" label="位置" align="center"></af-table-column>
                                    <af-table-column prop="HEALTHSTATUS" label="健康状态" align="center" :formatter="handlehealthstatus"></af-table-column>
                                    <af-table-column prop="RUNNINGSTATUS" label="运行状态" align="center" :formatter="handlerunningstatus"></af-table-column>
                                </el-table>
                            </div>

                        </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addportgroupVisible = false">取 消</el-button>
                <el-button type="primary" @click="createportgroup">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="执行结果" :visible.sync="addportgroupresultVisible" width="30%">
            <el-table
                    :data="portgroupresultData"
                    border
                    style="width: 100%"
            >
                <af-table-column prop="name" label="操作" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="reason" label="失败原因和建议" align="center"></af-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addportgroupresult">关闭</el-button>
            </span>
        </el-dialog>
        <el-dialog title="危险" :visible.sync="promptVisible" width="30%">
            <div class="prompt-border">
                <span>
                    您将要将LUN组({{lungroupname}})中的所有LUN映射给主机组（{{hostgroupname}}）中的所有主机。<br/>
                    如果主机组中存在多个主机且没有做好访问互斥，则多个业务主机向LUN写数据可能导致数据损坏或者不一致。<br/>
                    建议：执行该操作前请确认多个业务主机上已经做好访问互斥的配置。
                </span>
            </div>
            <el-row>
                <el-checkbox v-model="savemappingviewChecked" @change="handleCheckSelect">我已阅读上述信息，了解执行此操作带来的后果。</el-checkbox>
            </el-row>
            <span slot="footer" class="dialog-footer">
                <el-button @click="promptVisible = false">取 消</el-button>
                <el-button type="primary" :disabled="mappingSelectDisabled" @click="saveAddMappingViewList">确 定</el-button>
            </span>
        </el-dialog>
        <el-dialog title="执行结果" :visible.sync="addmappingviewresultVisible" width="30%">
            <el-table
                    :data="mappingviewresultData"
                    border
                    style="width: 100%"
            >
                <af-table-column prop="name" label="操作" align="center"></af-table-column>
                <af-table-column prop="status" label="状态" align="center"></af-table-column>
                <af-table-column prop="reason" label="失败原因和建议" align="center"></af-table-column>
            </el-table>
            <span slot="footer" class="dialog-footer">
                <el-button @click="addmappingviewresult">关闭</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    export default {
        name: "LunGroup",
        data() {
            return {
                addmappingVisible: false, // 创建时弹框的设置
                storageresult: {}, // 查询的存储的数据
                storage_env: '',
                tableData: [], // 查询一条存储返回的数据
                copytableData: [],
                storageHost: '',  // 存储搜索框默认显示的值
                mappingviewform: {},
                mappingviewrules: {
                    NAME: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ],
                    lungroupname: [
                        { required: true, message: '请选择LUN组', trigger: 'blur' },
                    ],
                    hostgroupname: [
                        { required: true, message: '请选择主机组', trigger: 'blur' },
                    ]
                },
                addmappingviewVisible: false,
                selectlungroupVisible: false,
                lungrouptableData: [],  // lungroup的查询结果
                lungroupchecked: true, //
                ISADD2MAPPINGVIEW:false,
                selectlungroupData: {},
                lunidchecked: false,
                startid: 0,
                lungroupname: '',
                selecthostgroupVisible: false,
                hostgrouptableData: [],
                hostgroupname: '',
                selecthostgroupData: {},
                portGroupChecked: false,
                portGroupDisabled: true,
                portgrouptableData: [],
                selectportgroupVisible: false,
                portgroupname: '',
                portgroupform: {},
                portrouprules: {
                    NAME: [
                        { required: true, message: '请输入名称', trigger: 'blur' },
                        { min: 1, max: 31, message: '请输入字母、数字、 “_”、“-”、 “.”和中文字符', trigger: 'blur' }
                    ],
                },
                addportgroupVisible: false,
                portGroupSearchName:'location',
                portGroupSearchValue:'',
                tableKey: 0,
                leftPortTableData: [],
                leftportData: [],
                selectedportList: [],
                selectedPorttableData: [],
                ETH_PORT: [],
                FC_PORT: [],
                FCoE_PORT: [],
                IB_PORT: [],
                typeSelect: '全部',
                healthSelect: '全部',
                runningSelect: '全部',
                allportList: [],
                hostData: [],  // 实时查询存储获取的数据
                mappingviewloading: false,  // 查询lun的列表时加载
                portrightSearchName: 'location',
                rightLocationValue: '',
                righttypeSelect: '全部',
                righthealthSelect: '全部',
                rightrunningSelect: '全部',
                allrightportList: [],
                portgroupresultData: [],
                addportgroupresultVisible: false,
                promptVisible: false, // 危险弹框提示
                savemappingviewChecked: false,
                mappingSelectDisabled: true,
                mappingviewresultData: [], //映射视图的执行结果
                addmappingviewresultVisible: false,
                mappingviewSearchName: 'name',
                nameSearchValue: '',
                idSearchValue: '',
                dangerTipDisabled: true,
                lungrouploading: false,
                lungroupSearch: 'name',
                namelungroupValue: '',
                idlungroupValue: '',
                copylungrouptableData: [],
                addlungroupDisabled: true,
                hostgrouploading:false,
                hostgroupSearch: 'name',
                namehostgroupValue: '',
                idhostgroupValue: '',
                copyhostgrouptableData: [],
                addhostgroupDisabled: true,
                portgrouploading: false,
                selectportgroupDisabled: true,
                copyportgrouptableData: [],
                portgroupSearch: 'name',
                nameportgroupValue: '',
                idportgroupValue: '',
                activeIndex: '1',
                mappingluntableData: [],
                mappinghosttableData: [],
                mappingporttableData: [],
                selectmappingview: {},
                groupInfo: [],
                grouptableData: [],
                groupname: '',
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getmappingviewList(){
                this.mappingviewloading = true
                this.$http.post( `automation/api/storage/mappingviewlist/`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.tableData = res.data;
                    this.copytableData = this.tableData
                    this.mappingviewloading = false
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data.msg))
                    this.mappingviewloading = false
                });
            },
            getData() {
                this.$http.get(`asset/api/storage/?current_page=1&pre_page=1`,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        if(res.data['data'].length!=0){
                            if(sessionStorage.getItem('storage_env')) {
                                this.storage_env = JSON.parse(sessionStorage.getItem('storage_env'));
                            }else {
                                sessionStorage.setItem('storage_env', JSON.stringify(res.data['data'][0]));
                                this.storage_env = res.data['data'][0];
                            }
                            this.storageresult = this.storage_env;
                            this.getmappingviewList();
                            this.storageHost = this.storage_env['hostname'] + '/' + this.storage_env['manage_ip'];
                        }else{
                            this.$message.error("未发现存储环境！")
                        }
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            handleAdd(){
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                this.mappingviewform = {}
                this.lungroupname = ''
                this.hostgroupname = ''
                this.portgroupname = ''
                this.portGroupChecked = false
                this.portGroupDisabled = true
                this.$http.post( `automation/api/storage/nextavailableid/?type=245`, {'manage_address': this.storageresult.manage_address,
                        'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                        let avaliableid = res['data']['ID']
                        avaliableid = parseInt(avaliableid) +1
                        let id_len = avaliableid.toString().length
                        if(id_len===1){
                            this.$set(this.mappingviewform, 'NAME', 'MappingView00'+avaliableid)
                        }else if(id_len===2){
                            this.$set(this.mappingviewform, 'NAME', 'MappingView0'+avaliableid)
                        }else{
                            this.$set(this.mappingviewform, 'NAME', 'MappingView'+avaliableid)
                        }
                        loading.close();
                        this.addmappingVisible = true;
                    }).catch( (error) => {
                        loading.close();
                        this.$message.error(JSON.stringify(error.response.data))
                    });
            },
            //查询lungroup
            getlungroupList(){
                this.$http.post( `automation/api/storage/lun_group_list/?ISADD2MAPPINGVIEW=${this.ISADD2MAPPINGVIEW}`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.lungrouptableData = res.data['data'];
                    this.copylungrouptableData = this.lungrouptableData
                    this.lungrouploading = false
                    this.selectlungroupVisible = true
                }).catch( (error) => {
                    this.lungrouploading = false
                    this.$message.error(JSON.stringify(error.response.data))
                });
            },
            //选择lungroup
            checklungroup(){
                this.lungrouploading = true
                this.addlungroupDisabled = true
                this.getlungroupList()
            },
            //添加lungroup
            addlungroup(){
                this.selectlungroupVisible = false
                if(this.mappingviewform.NAME&&this.lungroupname&&this.hostgroupname){
                    if(this.portGroupChecked){
                        if(this.portgroupname){
                            this.dangerTipDisabled = false
                        }
                    }else{
                        this.dangerTipDisabled = false
                    }
                }
            },
            // 查询是否归属于映射视图
            handlelungroup(){
                if(this.lungroupchecked===true){
                    this.ISADD2MAPPINGVIEW = false
                }else{
                    this.ISADD2MAPPINGVIEW = ''
                }
                this.getlungroupList()
            },
            //格式化是否属于映射
            handleISADD2MAPPINGVIEW(row){
                return row.ISADD2MAPPINGVIEW == 'false' ? '否' : row.ISADD2MAPPINGVIEW == 'true' ? '是':"";
            },
            // 选中lungroup时
            selectlungroup(row){
                this.selectlungroupData = row
                if(this.lunidchecked){
                    this.lungroupname = this.selectlungroupData.NAME + '(起始主机LUN ID: ' + this.startid + ')'
                }else{
                    this.lungroupname = this.selectlungroupData.NAME
                }
                this.addlungroupDisabled = false
            },
            //处理输入的起始id
            handlestartid(value){
                this.lungroupname = this.selectlungroupData.NAME + '(起始主机LUN ID: ' + value + ')'
            },
            //选择主机组
            selecthostgroup(row){
                this.selecthostgroupData = row
                this.hostgroupname = this.selecthostgroupData.NAME
                this.addhostgroupDisabled = false
            },
            //添加主机组
            addhostgroup(){
                this.selecthostgroupVisible = false
                if(this.mappingviewform.NAME&&this.lungroupname&&this.hostgroupname){
                    if(this.portGroupChecked){
                        if(this.portgroupname){
                            this.dangerTipDisabled = false
                        }
                    }else{
                        this.dangerTipDisabled = false
                    }
                }
            },
            //查询hostgroup
            gethostgroupList(){
                this.$http.post( `automation/api/storage/host_group_list/`, this.storageresult,{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.hostgrouptableData = res.data['data'];
                    this.copyhostgrouptableData = this.hostgrouptableData
                    this.hostgrouploading = false
                    this.selecthostgroupVisible = true
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data))
                });
            },
            //选择主机组
            checkhostgroup(){
                this.hostgrouploading = true
                this.addhostgroupDisabled = true
                this.gethostgroupList()
            },
            //修改端口组的状态
            selectPortGroupChecked(){
                if(this.portGroupChecked===true){
                    this.portGroupDisabled = false
                }else{
                    this.portGroupDisabled = true
                }
            },
            getportgroupList(){
                this.$http.post( `automation/api/storage/port_group_list/`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.portgrouptableData = res.data['data'];
                    this.copyportgrouptableData = this.portgrouptableData
                    this.portgrouploading = false
                    this.selectportgroupVisible = true
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data))
                });
            },
            checkportgroup(){
                this.portgrouploading = true
                this.selectportgroupDisabled = true
                this.getportgroupList()
            },
            selectportgroup(row){
                this.selectportgroupData = row
                this.portgroupname = this.selectportgroupData.NAME
                this.selectportgroupDisabled = false
            },
            addpostgroup(){
                this.selectportgroupVisible = false
                if(this.mappingviewform.NAME&&this.lungroupname&&this.hostgroupname){
                    if(this.portGroupChecked){
                        if(this.portgroupname){
                            this.dangerTipDisabled = false
                        }
                    }else{
                        this.dangerTipDisabled = false
                    }
                }
            },
            //左边表格选择项存入leftportData
            handleportgroupChange(rows){
                this.leftportData = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.leftportData.push(row);
                        }
                    });
                }
                console.log(this.leftportData, 555555)
            },
            //右边表格选择项存入selectedportList
            handleSelectedPortChange(rows){
                this.selectedportList = [];
                if (rows) {
                    rows.forEach(row => {
                        if (row) {
                            this.selectedportList.push(row);
                        }
                    });
                }
            },
            //创建端口
            Addport(){
                this.portgroupform = {}
                this.selectedPorttableData = []
                this.allportList = []
                this.leftportData = []
                this.selectedportList = []
                this.allrightportList = []
                const loading = this.$loading({
                    lock: true,
                    text: '拼命加载中',
                    spinner: 'el-icon-loading',
                });
                // 查询availidid
                this.$http.post( `automation/api/storage/nextavailableid/?type=257`, {'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let avaliableid = res['data']['ID']
                    avaliableid = parseInt(avaliableid) +1
                    let id_len = avaliableid.toString().length
                    if(id_len===1){
                        this.$set(this.portgroupform, 'NAME', 'PortGroup00'+avaliableid)
                    }else if(id_len===2){
                        this.$set(this.portgroupform, 'NAME', 'PortGroup0'+avaliableid)
                    }else{
                        this.$set(this.portgroupform, 'NAME', 'PortGroup'+avaliableid)
                    }
                    // 查询端口数据
                    this.$http.post(`automation/api/storage/portlist/`, {'manage_address': this.storageresult.manage_address,
                        'manage_username': this.storageresult.manage_username, 'manage_password': this.storageresult.manage_password},{headers:
                            {
                                'token': localStorage.getItem('token')
                            }}).then((res) =>{
                        this.ETH_PORT = res.data.ETH_PORT
                        this.FC_PORT = res.data.FC_PORT
                        this.FCoE_PORT = res.data.FCoE_PORT
                        this.IB_PORT = res.data.IB_PORT
                        console.log(this.ETH_PORT.length, this.FC_PORT.length, this.FCoE_PORT.length, this.IB_PORT.length)
                        this.leftPortTableData = this.ETH_PORT.concat(this.FC_PORT).concat(this.FCoE_PORT).concat(this.IB_PORT)
                        this.allportList = this.leftPortTableData
                        loading.close();
                        this.addportgroupVisible = true;
                    })
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data))
                });
            },
            getRowKeys(row) {
                return row.LOCATION+'/' + row.TYPE;
            },
            //左边表格项移动到右边
            addporttoright(){
                setTimeout(() => {
                    this.$refs["portTable"].clearSelection();
                    this.$refs["selectedportTable"].clearSelection();
                }, 0);
                this.leftportData.forEach(item => {
                    this.allrightportList.push(item);
                });
                this.selectedPorttableData = this.allrightportList
                for (let i = this.allportList.length-1; i >= 0; i--) {
                    for (let j = 0; j < this.leftportData.length; j++) {
                        if (
                            this.allportList[i] && this.leftportData[j]
                        ) {
                            let all_unique_val = this.allportList[i].LOCATION + '/' + this.allportList[i].TYPE
                            let left_unique_val = this.leftportData[j].LOCATION + '/' + this.leftportData[j].TYPE
                            if(all_unique_val === left_unique_val){
                                this.allportList.splice(i, 1);
                            }
                        }
                    }
                }
            },
            //表格右边移动到左边
            removeporttoleft(){
                setTimeout(() => {
                    this.$refs["portTable"].clearSelection();
                    this.$refs["selectedportTable"].clearSelection();
                }, 0);
                this.selectedportList.forEach(item => {
                    this.allportList.push(item);
                });
                this.leftPortTableData = this.allportList
                for (let i = this.allrightportList.length-1; i >=0 ; i--) {
                    for (let j = 0; j < this.selectedportList.length; j++) {
                        if (this.allrightportList[i] && this.selectedportList[j]) {
                            let all_unique_val = this.allrightportList[i].LOCATION + '/' + this.allrightportList[i].TYPE
                            let left_unique_val = this.selectedportList[j].LOCATION + '/' + this.selectedportList[j].TYPE
                            if(all_unique_val === left_unique_val){
                                this.allrightportList.splice(i, 1);
                            }
                        }
                    }
                }
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

                sessionStorage.setItem('storage_env', JSON.stringify(row));
                this.storageHost = row.hostname + '/' + row.manage_ip;
                this.storageresult = row;
                this.tableData = [];
                this.getmappingviewList();
            },
            handletype(row){
                return row.TYPE == 213 ? '以太网端口' : row.TYPE == 212 ? 'FC端口': row.TYPE == 252 ? "FCoE端口" : row.TYPE == 16500 ?'IB端口': '';
            },
            handlehealthstatus(row){
                return row.HEALTHSTATUS == '0' ? '未知' : row.HEALTHSTATUS == '1' ? '正常': row.HEALTHSTATUS == '2' ? '故障':
                    row.HEALTHSTATUS == '3'? '即将故障': row.HEALTHSTATUS == '9'? '不一致':'';
            },
            //处理运行状态
            handlerunningstatus(row){
                return row.RUNNINGSTATUS == '0' ? '未知': row.RUNNINGSTATUS == '1'? '正常' : row.RUNNINGSTATUS == '2' ? '运行':
                    row.RUNNINGSTATUS == '10' ? '已连接':row.RUNNINGSTATUS == '11' ? '未连接':'';
            },
            //处理运行状态
            handlelunrunningstatus(row){
                return row.RUNNINGSTATUS == '53' ? '初始化中': row.RUNNINGSTATUS == '27'? '在线' : row.RUNNINGSTATUS == '28' ? '离线': '';
            },
            handlehostrunningstatus(row){
                return row.RUNNINGSTATUS == '1' ? '正常': '';
            },
            queryleftportData(){
                if(this.portGroupSearchName==='location'){
                    if(this.portGroupSearchValue!=''){
                        this.leftPortTableData = []
                        this.allportList.forEach((item)=>{
                             let incledes_res = item.LOCATION.includes(this.portGroupSearchValue);
                            if(incledes_res===true){
                                this.leftPortTableData.push(item)
                            }
                        })
                    }else{
                        this.leftPortTableData = this.allportList
                    }
                    }else if(this.portGroupSearchName==='type'){
                        if(this.typeSelect==='全部'|| this.typeSelect==='all'){
                            this.leftPortTableData = this.allportList
                        }else{
                            this.leftPortTableData = []
                            console.log(this.allportList)
                            this.allportList.forEach((item)=>{
                                let incledes_res = item.TYPE.toString().includes(this.typeSelect);
                                if(incledes_res===true){
                                    this.leftPortTableData.push(item)
                                }
                            })
                        }
                    }else if(this.portGroupSearchName==='health'){
                        if(this.healthSelect==='全部'|| this.healthSelect==='all'){
                            this.leftPortTableData = this.allportList
                        }else{
                            this.leftPortTableData = []
                            this.allportList.forEach((item)=>{
                                let incledes_res = item.HEALTHSTATUS.includes(this.healthSelect);
                                if(incledes_res===true){
                                    this.leftPortTableData.push(item)
                                }
                            })
                        }
                    }else if(this.portGroupSearchName==='running'){
                        if(this.runningSelect==='全部'|| this.runningSelect==='all'){
                            this.leftPortTableData = this.allportList
                        }else{
                            this.leftPortTableData = []
                            this.allportList.forEach((item)=>{
                                let incledes_res = item.RUNNINGSTATUS.includes(this.runningSelect);
                                if(incledes_res===true){
                                    this.leftPortTableData.push(item)
                                }
                            })
                        }
                }
            },
            queryrightportData(){
                if(this.portrightSearchName==='location'){
                    if(this.rightLocationValue!=''){
                        this.selectedPorttableData = []
                        this.allrightportList.forEach((item)=>{
                            let incledes_res = item.LOCATION.includes(this.rightLocationValue);
                            if(incledes_res===true){
                                this.selectedPorttableData.push(item)
                            }
                        })
                    }else{
                        this.selectedPorttableData = this.allrightportList
                    }
                }else if(this.portrightSearchName==='type'){
                    if(this.righttypeSelect==='全部'|| this.righttypeSelect==='all'){
                        this.selectedPorttableData = this.allrightportList
                    }else{
                        this.selectedPorttableData = []
                        this.allrightportList.forEach((item)=>{
                            let incledes_res = item.TYPE.toString().includes(this.righttypeSelect);
                            if(incledes_res===true){
                                this.selectedPorttableData.push(item)
                            }
                        })
                    }
                }else if(this.portrightSearchName==='health'){
                    if(this.righthealthSelect==='全部'|| this.righthealthSelect==='all'){
                        this.selectedPorttableData = this.allrightportList
                    }else{
                        this.selectedPorttableData = []
                        this.allrightportList.forEach((item)=>{
                            let incledes_res = item.HEALTHSTATUS.includes(this.righthealthSelect);
                            if(incledes_res===true){
                                this.selectedPorttableData.push(item)
                            }
                        })
                    }
                }else if(this.portrightSearchName==='running'){
                    if(this.rightrunningSelect==='全部'|| this.rightrunningSelect==='all'){
                        this.selectedPorttableData = this.allrightportList
                    }else{
                        this.selectedPorttableData = []
                        this.allrightportList.forEach((item)=>{
                            let incledes_res = item.RUNNINGSTATUS.includes(this.rightrunningSelect);
                            if(incledes_res===true){
                                this.selectedPorttableData.push(item)
                            }
                        })
                    }
                }
            },
            saveAddMappingViewList(){
                console.log(this.selecthostgroupData, 'hostgroup')
                console.log(this.selectlungroupData, 'lungroup')
                console.log(this.selectportgroupData, 'portgroup')
                console.log(this.mappingviewform, 'mappingviewform')
                this.mappingviewresultData = []
                let name = "创建映射视图 " + this.mappingviewform.NAME
                let add_res = {'name': name, 'status': '正在执行', 'reason': ''}
                this.mappingviewresultData.push(add_res)
                if(this.selecthostgroupData){
                    let host_name = "增加主机组 " + this.selecthostgroupData.NAME
                    this.mappingviewresultData.push({'name': host_name, 'status': '等待执行', 'reason': '','id': this.selecthostgroupData.ID, 'type': this.selecthostgroupData.TYPE})
                }
                if(this.selectlungroupData){
                    let lun_name = "增加LUN组 " + this.selectlungroupData.NAME
                    this.mappingviewresultData.push({'name': lun_name, 'status': '等待执行', 'reason': '','id': this.selectlungroupData.ID, 'type': this.selectlungroupData.TYPE})
                }
                if(this.selectportgroupData){
                    let port_name = "增加端口组 " + this.selectportgroupData.NAME
                    this.mappingviewresultData.push({'name': port_name, 'status': '等待执行', 'reason': '','id': this.selectportgroupData.ID, 'type': this.selectportgroupData.TYPE})
                }

                this.addmappingviewresultVisible = true
                this.create_mapping_view()
            },
            create_mapping_view(){
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
                this.$http.post(`automation/api/storage/create_mapping_view/`, {'mapping_view': this.mappingviewform, 'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                    'manage_address': this.storageresult.manage_address}, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let mapping_view_data = res.data
                    if(res.status===200){
                        this.mappingviewresultData[0].status = '成功'
                    }
                    if(mapping_view_data){
                        CustomForeach(this.mappingviewresultData, async (e, i) => {
                            if(i>0){
                                await this.mappingviewassociate(e, mapping_view_data.ID);
                            }
                        });
                    }
                }).catch( (error)=> {
                    this.mappingviewresultData[0].status = '执行失败'
                    this.mappingviewresultData[0].reason = error.response.data.msg
                    this.$message.error(JSON.stringify(error.response.data.msg));
                });
            },
            mappingviewassociate(add_res, group_id){
                return new Promise((resolve, reject) => {
                    add_res.status = '正在执行'
                    this.$http.post(`automation/api/storage/mapping_view_associate/`, {
                        'mapping_associate':{'ID': group_id, "ASSOCIATEOBJTYPE": add_res.type, "ASSOCIATEOBJID": add_res.id},  'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                        'manage_address': this.storageresult.manage_address, 'HOSTLUNID': this.startid
                    }, {
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
            dangerTip(){
                this.promptVisible = true
            },
            //创建端口组
            createportgroup(){
                this.portgroupresultData = []
                let name = "创建端口组 " + this.portgroupform.NAME
                let add_res = {'name': name, 'status': '正在执行', 'reason': ''}
                this.portgroupresultData.push(add_res)
                for (var i=0;i<this.allrightportList.length;i++)
                {
                    let type = ''
                    if(this.allrightportList[i].TYPE===213){
                        type = '以太网端口'
                    }else if(this.allrightportList[i].TYPE===212){
                        type = 'FC端口'
                    }else if(this.allrightportList[i].TYPE===252){
                        type = 'FCoE端口'
                    }else if(this.allrightportList[i].TYPE===16500){
                        type = 'IB端口'
                    }
                    let port_name = "增加端口 " + type + ':' + this.allrightportList[i].LOCATION
                    this.portgroupresultData.push({'name': port_name, 'status': '等待执行', 'reason': '','port_id': this.allrightportList[i].ID,
                        'port_type': this.allrightportList[i].TYPE})
                }
                this.addportgroupresultVisible = true
                this.create_port_group()
            },
            create_port_group(){
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
                this.$http.post(`automation/api/storage/create_port_group/`, {'port_group': this.portgroupform, 'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                    'manage_address': this.storageresult.manage_address}, {
                    headers:{
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    let port_group_data = res.data
                    if(res.status===200){
                        this.portgroupresultData[0].status = '成功'
                    }else{
                        this.portgroupresultData[0].status = '执行失败'
                        this.portgroupresultData[0].reason = res.data
                    }
                    if(port_group_data){
                        CustomForeach(this.portgroupresultData, async (e, i) => {
                            if(i>0){
                                await this.portgroupassociate(e, port_group_data.ID);
                            }
                        });
                    }
                })

            },
            portgroupassociate(add_res, group_id){
                return new Promise((resolve, reject) => {
                    // this.portgroupform.NAME = add_res.real_name
                    add_res.status = '正在执行'
                    this.$http.post(`automation/api/storage/port_group_associate/`, {
                        'port_associate':{'ID': group_id, "ASSOCIATEOBJTYPE": add_res.port_type, "ASSOCIATEOBJID": add_res.port_id}, 'manage_username': this.storageresult.manage_username,'manage_password': this.storageresult.manage_password,
                        'manage_address': this.storageresult.manage_address
                    }, {
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
            //执行结果点击关闭时
            addportgroupresult(){
                this.addportgroupresultVisible = false
                this.addportgroupVisible = false
            },
            addmappingviewresult(){
                this.addmappingviewresultVisible = false
                this.promptVisible = false
                this.addmappingVisible = false
                this.getmappingviewList()
            },
            // 处理危险弹框
            handleCheckSelect(){
                this.mappingSelectDisabled = !this.mappingSelectDisabled
            },
            //按条件查询
            querymappingview(){
                if(this.mappingviewSearchName==='name'){
                    if(this.nameSearchValue!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.nameSearchValue);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }else if(this.mappingviewSearchName==='id'){
                    if(this.idSearchValue!=''){
                        this.tableData = []
                        this.copytableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.idSearchValue);
                            if(incledes_res===true){
                                this.tableData.push(item)
                            }
                        })
                    }else{
                        this.tableData = this.copytableData
                    }
                }
            },
            querylungroup(){
                if(this.lungroupSearch==='name'){
                    if(this.namelungroupValue!=''){
                        this.lungrouptableData = []
                        this.copylungrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.namelungroupValue);
                            if(incledes_res===true){
                                this.lungrouptableData.push(item)
                            }
                        })
                    }else{
                        this.lungrouptableData = this.copylungrouptableData
                    }
                }else if(this.lungroupSearch==='id'){
                    if(this.idlungroupValue!=''){
                        this.lungrouptableData = []
                        this.copylungrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.idlungroupValue);
                            if(incledes_res===true){
                                this.lungrouptableData.push(item)
                            }
                        })
                    }else{
                        this.lungrouptableData = this.copylungrouptableData
                    }
                }
            },
            queryhostgroup(){
                if(this.hostgroupSearch==='name'){
                    if(this.namehostgroupValue!=''){
                        this.hostgrouptableData = []
                        this.copyhostgrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.namehostgroupValue);
                            if(incledes_res===true){
                                this.hostgrouptableData.push(item)
                            }
                        })
                    }else{
                        this.hostgrouptableData = this.copyhostgrouptableData
                    }
                }else if(this.hostgroupSearch==='id'){
                    if(this.idhostgroupValue!=''){
                        this.hostgrouptableData = []
                        this.copyhostgrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.idhostgroupValue);
                            if(incledes_res===true){
                                this.hostgrouptableData.push(item)
                            }
                        })
                    }else{
                        this.hostgrouptableData = this.copyhostgrouptableData
                    }
                }
            },
            queryportgroup(){
                if(this.portgroupSearch==='name'){
                    if(this.nameportgroupValue!=''){
                        this.portgrouptableData = []
                        this.copyportgrouptableData.forEach((item)=>{
                            let incledes_res = item.NAME.includes(this.nameportgroupValue);
                            if(incledes_res===true){
                                this.portgrouptableData.push(item)
                            }
                        })
                    }else{
                        this.portgrouptableData = this.copyportgrouptableData
                    }
                }else if(this.portgroupSearch==='id'){
                    if(this.idportgroupValue!=''){
                        this.portgrouptableData = []
                        this.copyportgrouptableData.forEach((item)=>{
                            let incledes_res = item.ID.includes(this.idportgroupValue);
                            if(incledes_res===true){
                                this.portgrouptableData.push(item)
                            }
                        })
                    }else{
                        this.portgrouptableData = this.copyportgrouptableData
                    }
                }
            },
            handleStepOPtions(){
                this.grouptableData = []
                this.groupname = ''
                if(this.selectmappingview.NAME){
                    if(this.activeIndex==='1'){
                        this.getgroupList(256,this.selectmappingview.TYPE, this.selectmappingview.ID)
                    }else if(this.activeIndex==='2'){
                        this.getgroupList(14,this.selectmappingview.TYPE, this.selectmappingview.ID)
                    }else if(this.activeIndex==='3'){
                        this.getgroupList(257,this.selectmappingview.TYPE, this.selectmappingview.ID)
                    }
                }
            },
            selectmapping(row){
                this.selectmappingview = row
                if(this.activeIndex==='1'){
                    this.getgroupList(256,row.TYPE, row.ID)
                }else if(this.activeIndex==='2'){
                    this.getgroupList(14,row.TYPE, row.ID)
                }else if(this.activeIndex==='3'){
                    this.getgroupList(257,row.TYPE, row.ID)
                }
            },
            getgroupList(type, ASSOCIATEOBJTYPE, ASSOCIATEOBJID) {
                this.$http.post(`automation/api/storage/associate_mappingview/?TYPE=${type}&ASSOCIATEOBJTYPE=${ASSOCIATEOBJTYPE}&ASSOCIATEOBJID=${ASSOCIATEOBJID}`, {
                    'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username,
                    'manage_password': this.storageresult.manage_password
                }, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    console.log(res, 44444)
                    if(res.data){
                        this.groupInfo = res.data;
                        this.groupname = this.groupInfo[0].NAME
                        let type_ = 0
                        if (type === 256) {
                            type_ = 11
                        } else if (type === 14) {
                            type_ = 21
                        }
                        this.associate_group(type_)
                    }else{
                        this.groupname = ''
                        this.grouptableData = []
                    }
                }).catch((error) => {
                    console.log(33333)
                    this.$message.error(JSON.stringify(error.response.data.msg))
                    this.grouptableData = []
                });
            },
            associate_group(type_){
                this.$http.post(`automation/api/storage/associate_group/?TYPE=${type_}&ASSOCIATEOBJTYPE=${this.groupInfo[0].TYPE}&ASSOCIATEOBJID=${this.groupInfo[0].ID}`, {
                    'manage_address': this.storageresult.manage_address,
                    'manage_username': this.storageresult.manage_username,
                    'manage_password': this.storageresult.manage_password
                }, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    this.grouptableData = res.data
                })
            },
            handlehostlunid(row){
                if(row.ASSOCIATEMETADATA!=undefined){
                    return JSON.parse(row.ASSOCIATEMETADATA).HostLUNID
                }
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
            handleoperationsystem(row){
                return row.OPERATIONSYSTEM == '0'? 'Linux' : row.OPERATIONSYSTEM == '1'? 'Windows': row.OPERATIONSYSTEM == '2'? 'Solaris':
                    row.OPERATIONSYSTEM == '3'? 'HP-UX': row.OPERATIONSYSTEM == '4'? 'AIX': row.OPERATIONSYSTEM == '5'? 'XenServer':
                        row.OPERATIONSYSTEM == '6'? 'Mac OS': row.OPERATIONSYSTEM == '7'? 'VMware ESX': row.OPERATIONSYSTEM == '8'? 'LINUX_VIS':
                            row.OPERATIONSYSTEM == '9'?'Windows Server 2012':row.OPERATIONSYSTEM == '10'? 'Oracle VM':
                                row.OPERATIONSYSTEM == '11'?'OpenVMS': ''
            }
        }
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";

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
    .portcheck{
        color:#ccc;
    }
    .portcheck /deep/ .el-checkbox__input{
        top: -30px;
        left: 32px;
    }
    .portItem /deep/ .el-form-item__label{
        color:#cccc;
    }
    .portgroup_create_p{
        border-bottom: 1px solid #C0C4CC;
        padding-bottom: 6px;
        margin-bottom: 10px;
    }
    .div-height{
        height: 280px;
        overflow: auto;
    }
    .prompt-border {
        height: 130px;
        padding: 10px;
        border: 1px solid #c5c3c3
    }

</style>

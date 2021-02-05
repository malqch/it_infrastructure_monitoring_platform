<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
            </el-breadcrumb>
        </div>
        <div class="container">
            <div style="margin-bottom: 15px;">
                <span>华为云环境：</span>
                <el-select v-model="huaweiyun_env" @change="handleSelectHuaweiEnv" style="width: 130px;" placeholder="请选择华为云环境">
                    <el-option
                            v-for="item in huaweiyun_options"
                            :key="item.id"
                            :label="item.hw_ip"
                            :value="item.hw_ip">
                    </el-option>
                </el-select>
            </div>
            <el-row type="flex" class="row-bg" justify="space-between">
                <div>
                    <el-button
                            type="primary"
                            icon="el-icon-circle-plus-outline"
                            @click="handleCreate">创建虚拟机</el-button>
                </div>
                <div>
                    <el-input
                            type="text"
                            placeholder="请输入虚拟机名称"
                            v-model="keywords"
                            style="width:200px; margin-bottom:15px;" clearable>
                    </el-input>
                    <el-button style="margin-left:10px;" type="primary" @click="handleSearch">查询</el-button>
                </div>
            </el-row>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%"
                    max-height="600"
            >
<!--                <el-table-column type="selection" align="center"></el-table-column>-->
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <el-table-column prop="name" label="名称" align="center"></el-table-column>
                <el-table-column prop="id" label="ID" align="center"></el-table-column>
                <el-table-column prop="status" label="状态" :formatter="statusFormat" align="center"></el-table-column>
                <el-table-column prop="vmType" label="类型" :formatter="typeFormat" align="center"></el-table-column>
                <el-table-column prop="arch" label="CPU架构" align="center"></el-table-column>
<!--                <el-table-column prop="param" label="CPU占用率" align="center"></el-table-column>-->
<!--                <el-table-column prop="test_status" label="内存占用率" align="center"></el-table-column>-->
<!--                <el-table-column prop="test_status" label="磁盘占用率" align="center"></el-table-column>-->
                <el-table-column prop="ip" label="IP地址" align="center"></el-table-column>
                <el-table-column prop="clusterName" label="所属集群" align="center"></el-table-column>
                <el-table-column prop="hostName" label="所属主机" align="center"></el-table-column>
                <el-table-column label="操作" width="250" align="center">
                    <template slot-scope="scope">
                        <el-button
                                v-if="scope.row.status ==='stopped'"
                                type="text"
                                icon="el-icon-edit"
                                @click="handleStartVms(scope.$index, scope.row)"
                        >启动</el-button>
                        <el-button
                                v-if="scope.row.status ==='running'"
                                type="text"
                                icon="el-icon-edit"
                                @click="handleStopVms(scope.$index, scope.row)"
                        >停止</el-button>
                        <el-button
                                type="text"
                                icon="el-icon-delete"
                                class="red"
                                @click="handleDeleteVms(scope.$index, scope.row)"
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
        <!-- 创建虚拟机弹框 -->
        <el-dialog title="创建虚拟机" :visible.sync="editVisible" :close-on-click-modal="false" width="65%">
            <div class="vm-dialog-div">
                <el-form ref="form" :rules="rules" :model="form" label-width="100px" labelPosition="left">
                <el-row :span="24">
                    <el-col :span="6">
                    <div class="border-left">
                        <el-steps direction="vertical" :active="active" finish-status="success">
                            <el-step v-for="item in step_options"
                                     :key="item.value"
                                     :title="item.label"></el-step>
                        </el-steps>
                    </div>
                    </el-col>
                    <el-col :span="18">
                        <el-row v-if="this.active===0">
                            <span style="margin-left: 20px;">您要如何创建虚拟机？</span>
                            <div  class="border-right">
                                <el-tabs v-model="activeName"
                                         tab-position="left"
                                         style="height: 200px;"
                                         type="card"
                                         @tab-click="handleStepOPtions">
                                    <el-tab-pane label="创建新虚拟机" name="0">此选项将指导您完成创建新虚拟机的过程。您将可以自定义CPU、内存、网卡和磁盘。创建之后将需要安装客户机操作系统。</el-tab-pane>
                                    <el-tab-pane label="使用模板部署虚拟机" name="1">此选项将指导您完成从模板部署虚拟机的过程。模板是最佳配置的虚拟机映像，使您轻松创建可以立即使用的虚拟机。您必须具有一个模板才能继续使用此选项。</el-tab-pane>
<!--                                    <el-tab-pane label="模板转为虚拟机" name="2">此选项将指导您完成将模板转化为一个虚拟机。</el-tab-pane>-->
                                </el-tabs>
                            </div>
                        </el-row>
                        <div  class="border-right-next">
                        <el-row v-if="this.activeName==='0'">
                            <el-row v-if="this.active===1">
                                    <el-form-item label="名称：" prop="name" label-width="150px">
                                        <el-input v-model="form.name" class="create-input"></el-input>
                                    </el-form-item>
                                    <el-form-item label="描述：" prop="description" label-width="150px">
                                        <el-input type="textarea" v-model="form.descripttion" class="create-input"></el-input>
                                    </el-form-item>
                                    <el-form-item label="选择虚拟机位置：" prop="parentObjUrn" label-width="150px">
                                        <el-input v-model="parentObjUrnTo" class="create-input" disabled></el-input>
                                        <el-button @click="handleSelectPosition">选择</el-button>
                                    </el-form-item>
                                    <el-form-item label="选择计算资源：" prop="location" label-width="150px">
                                        <el-input v-model="locationTo" class="create-input" disabled></el-input>
                                        <el-button @click="handleSelectCluster">选择</el-button>
                                        <el-checkbox v-model="form.isBindingHost" style="padding-left: 15px;" :disabled="checked_disabled">与所选主机绑定</el-checkbox>
                                    </el-form-item>
                                    <el-form-item label="操作系统类型：" label-width="150px">
                                        <el-radio-group v-model="form.osOptions.osType" @change="selectOsType">
                                            <el-radio v-for="item in os_type_arr"
                                                      :key="item.id"
                                                      :label="item.label">{{item.label}}</el-radio>
                                        </el-radio-group>
                                    </el-form-item>
                                    <el-form-item label="操作系统版本号：" label-width="150px">
                                        <el-select v-model="form.osOptions.osVersion" filterable placeholder="请选择操作系统版本" class="create-input">
                                            <el-option
                                                    v-for="item in os_version_options"
                                                    :key="item.os_id"
                                                    :label="item.os_version"
                                                    :value="item.os_id">
                                            </el-option>
                                        </el-select>
                                    </el-form-item>
                                    <el-form-item v-if="form.osOptions.osType==='其他'" label="操作系统名称：" label-width="150px">
                                        <el-input v-model="form.osOptions.osName" class="create-input"></el-input>
                                    </el-form-item>
                                </el-row>
                            <el-row v-else-if="this.active===2">
                                <el-table
                                        ref="singleTable"
                                        :data="storeTableData"
                                        border
                                        style="width:100%"
                                        highlight-current-row
                                        max-height="600"
                                        @current-change="handleSelectionChange"
                                >
                                    <el-table-column prop="name" label="名称" align="center"></el-table-column>
                                    <el-table-column prop="actualFreeSizeGB" label="可用容量(GB)" align="center"></el-table-column>
<!--                                    <el-table-column prop="userType" label="使用方式" align="center"></el-table-column>-->
                                    <el-table-column prop="storageType" :formatter="storageTypeFormat" label="类型" align="center"></el-table-column>
                                </el-table>
                            </el-row>
                            <el-row v-else-if="this.active===3">
                                <el-tabs v-model="activeVMName" @tab-click="handleVMClick">
                                    <el-tab-pane label="硬件" name="0">
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showCPUInfo" :class="cpu_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="CPU" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.cpu.quantity" @change="handleCPUChange" style="width: 200px;" :min="1" :max="36"></el-input-number>
                                                    <el-tooltip class="item" effect="dark" placement="right">
                                                        <div slot="content">范围: 1-36<br/>建议虚拟机的内核数是每个插槽的内核数<br/>的整数倍。</div>
                                                        <i class="el-icon-warning bluecolor"></i>
                                                    </el-tooltip>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_cpu">
                                                        <!--                                                    <el-form-item label="CPU绑定" label-width="160px">-->
                                                        <!--                                                        <el-switch-->
                                                        <!--                                                                v-model="form.cpu_band"-->
                                                        <!--                                                                @change="handleBandCategory"-->
                                                        <!--                                                                active-color="#13ce66">-->
                                                        <!--                                                        </el-switch>-->
                                                        <!--                                                    </el-form-item>-->
                                                        <!--                                                    <el-form-item label="CPU线程绑定策略">-->
                                                        <!--                                                        <el-select :disabled="cpu_disabled" v-model="form.cpu_band_category" placeholder="请选择绑定策略">-->
                                                        <!--                                                            <el-option-->
                                                        <!--                                                                    v-for="item in cpu_band_category_options"-->
                                                        <!--                                                                    :key="item"-->
                                                        <!--                                                                    :label="item"-->
                                                        <!--                                                                    :value="item">-->
                                                        <!--                                                            </el-option>-->
                                                        <!--                                                        </el-select>-->
                                                        <!--                                                    </el-form-item>-->
                                                        <el-form-item label="份额" label-width="135px">
                                                            <el-select v-model="cpu_share" @change="handleCpuShare" placeholder="份额" style="width: 100px;">
                                                                <el-option
                                                                        v-for="item in cpu_share_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-input :disabled="cpu_share_disabled" v-model="form.vmConfig.cpu.weight" style="width: 100px;"></el-input>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">描述：定义多个虚拟机在竞争物理CPU资<br/>源时按比例分配，份额越高的虚拟机，竞<br/>争物理CPU时获取的资源越多。 <br/>范围：<br/>
                                                                    低：内核数*250<br/>
                                                                    中：内核数*500<br/>
                                                                    高：内核数*1000<br/>
                                                                    自定义：2~255000</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="每个插槽内核数" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.coresPerSocket" style="width: 200px;" :min="1" :max="36"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 1-36<br/>插槽数:{{Math.ceil(form.vmConfig.cpu.quantity/form.vmConfig.cpu.coresPerSocket)}}</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="预留(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.reservation" style="width: 200px;" :min="0" :max="4400"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 0-{{form.vmConfig.cpu.quantity*2200}}<br/>
                                                                    定义了多个虚拟机竞争物理CPU资源的时<br/>候分配的最低计算资源。如果指定CPU的<br/>预留值，需要排除故障和已经停止的主<br/>机。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="限制(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.limit" style="width: 200px;" :min="0" :max="4400"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">0表示不限<br/>
                                                                    控制虚拟机占用物理CPU资源的上限。以<br/>一个两CPU的虚拟机为例，如果设置该虚<br/>拟机CPU上限为3000MHz，则该虚拟机的<br/>两个虚拟CPU计算能力被限制为<br/>1500MHz。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showMemInfo" :class="mem_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="内存" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.memory.quantityMB" @change="handleMemChange" style="width: 200px;" :min="1" :max="4096"></el-input-number>
                                                    <el-button type="primary" style="margin-left: 5px;">GB</el-button>
                                                    <el-tooltip class="item" effect="dark" placement="right">
                                                        <div slot="content">32位系统无法充分利用4G内存，建议32<br/>位系统无需配满4G内存，可以配置<br/>3583MB内存（约3.5GB）。</div>
                                                        <i class="el-icon-warning" style="color:#66b1ff;"></i>
                                                    </el-tooltip>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_mem">
                                                        <!--                                                <el-form-item label="大页配置">-->
                                                        <!--                                                    <el-select v-model="form.large_page_config" @change="handleLargePageConfig" placeholder="大页配置">-->
                                                        <!--                                                        <el-option-->
                                                        <!--                                                                v-for="item in large_page_config_options"-->
                                                        <!--                                                                :key="item"-->
                                                        <!--                                                                :label="item"-->
                                                        <!--                                                                :value="item">-->
                                                        <!--                                                        </el-option>-->
                                                        <!--                                                    </el-select>-->
                                                        <!--                                                </el-form-item>-->
                                                        <el-form-item label="份额" label-width="135px">
                                                            <el-select v-model="mem_share" @change="handleMemShare" placeholder="份额" style="width: 100px;">
                                                                <el-option
                                                                        v-for="item in cpu_share_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-input v-model="form.vmConfig.memory.weight" :disabled="mem_share_disabled" class="create-input" style="width: 100px;"></el-input>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">低：内存大小 * 5<br/>
                                                                    中：内存大小 * 10<br/>
                                                                    高：内存大小 * 20<br/>
                                                                    自定义：1~83886080</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="预留(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.memory.reservation" :disabled="mem_reserve_disabled" style="width: 200px;" :min="0" :max="4096"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 0-{{form.vmConfig.memory.quantityMB*1024}}<br/>
                                                                    当集群的内存复用开启时,内存预留值生<br/>效;<br/>
                                                                    具有PCI直通设备(包括SRIOV)的虚拟机<br/>或是虚拟机所在主机配置了内存盘模式，<br/>内存预留值必须和内存规格值相等，即必<br/>须全预留。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="限制(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.memory.limit" :disabled="mem_limit_disabled" style="width: 200px;" :min="0" :max="4096"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: {{form.vmConfig.memory.quantityMB*1024}}-{{form.vmConfig.memory.quantityMB*1024}}, 0表示不限</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showDiskInfo" :class="disk_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="磁盘1" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.disks[0].quantityGB" @change="handleCPUChange" style="width: 200px;" :min="1" :max="1024"></el-input-number>
                                                    <el-button type="primary" style="margin-left: 5px;">GB</el-button>
                                                    <el-tooltip class="item" effect="dark" placement="right">
                                                        <div slot="content">如需指定系统盘，需要精确指定虚拟机设<br/>备启动顺序，可以在选项->系统->启动方<br/>式指定启动顺序。</div>
                                                        <i class="el-icon-warning" style="color:#66b1ff;"></i>
                                                    </el-tooltip>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_disk">
                                                        <el-form-item label="数据存储" prop="dataStore" label-width="135px">
                                                            <el-input v-model="form.vmConfig.disks[0].name" style="width: 150px;" disabled></el-input>
                                                            <el-button @click="handleSelectDataStore">选择</el-button>
                                                        </el-form-item>
                                                        <el-form-item label="配置模式" label-width="135px">
                                                            <el-select v-model="form.vmConfig.disks[0].volType" @change="handleSelectVolType" placeholder="配置模式">
                                                                <el-option
                                                                        v-for="item in config_mode_options"
                                                                        :key="item.value"
                                                                        :label="item.name"
                                                                        :value="item.value">
                                                                </el-option>
                                                            </el-select>
                                                        </el-form-item>
                                                        <!--                                                <el-form-item label="磁盘模式">-->
                                                        <!--                                                    <el-select v-model="form.disk_mode" placeholder="磁盘模式" style="width: 200px;">-->
                                                        <!--                                                        <el-option-->
                                                        <!--                                                                v-for="item in disk_mode_options"-->
                                                        <!--                                                                :key="item"-->
                                                        <!--                                                                :label="item"-->
                                                        <!--                                                                :value="item">-->
                                                        <!--                                                        </el-option>-->
                                                        <!--                                                    </el-select>-->
                                                        <!--                                                </el-form-item>-->
                                                        <el-form-item label="总线类型" label-width="135px">
                                                            <el-select v-model="form.vmConfig.disks[0].pciType" placeholder="总线类型">
                                                                <el-option
                                                                        v-for="item in bus_type_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">VIRTIO/IDE/SCSI :创建虚拟机时，数据<br/>存储上创建的磁盘可以挂载在VIRTIO、<br/>IDE、SCSI总线上，VIRTIO性能较好，<br/>IDE性能较差，仅用于虚拟机镜像制作及<br/>虚拟机光驱。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showNetworkInfo" :class="network_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="网卡1" label-width="135px">
                                                    <el-input v-model="portGroupUrnTo" style="width: 150px;" disabled></el-input>
                                                    <el-button @click="handleNetworkSwitch">选择</el-button>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_network">
                                                        <el-form-item label="网卡类型" label-width="135px">
                                                            <el-select v-model="form.vmConfig.nics[0].virtIo" placeholder="网卡类型">
                                                                <el-option
                                                                        v-for="item in network_type_options"
                                                                        :key="item.value"
                                                                        :label="item.name"
                                                                        :value="item.value">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">virtio : 高网络吞吐量和降低网络延迟的网<br/>卡类型。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="IO环大小" label-width="135px">
                                                            <el-select v-model="form.vmConfig.nics[0].nicConfig.vringbuf" placeholder="IO环大小">
                                                                <el-option
                                                                        v-for="item in IO_ring_num_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">通过适当的调大IO环，可以缓解前端驱动<br/>的丢包，提高性能。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="队列数" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.nics[0].nicConfig.queues" @change="handleCPUChange" style="width: 210px;" :min="1" :max="form.vmConfig.cpu.quantity"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">队列数取值不能超过虚拟机当前的vCPU<br/>数量。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="开启安全组" label-width="135px">
                                                            <el-switch
                                                                    v-model="form.vmConfig.nics[0].enableSecurityGroup"
                                                                    active-color="#13ce66"
                                                                    @change="handleSwitchSecurityGroup">
                                                            </el-switch>
                                                        </el-form-item>
                                                        <el-form-item v-if="form.vmConfig.nics[0].enableSecurityGroup" label="安全组" label-width="135px">
                                                            <el-input v-model="form.vmConfig.nics[0].securityGroupId" style="width: 150px;"></el-input>
                                                            <el-button @click="handleSelectSecurityGroup">选择</el-button>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
<!--                                        <el-form-item label="显卡">-->
<!--                                            <el-select v-model="form.gpu" @change="handleSelectGpuSize" placeholder="请选择显卡" style="width: 100px;">-->
<!--                                                <el-option-->
<!--                                                        v-for="item in gpu_options"-->
<!--                                                        :key="item"-->
<!--                                                        :label="item"-->
<!--                                                        :value="item">-->
<!--                                                </el-option>-->
<!--                                            </el-select>-->
<!--                                            <el-select v-model="form.gpu_size" placeholder="请选择显卡大小" style="width: 100px; padding-left: 10px;">-->
<!--                                                    <el-option-->
<!--                                                            v-for="item in gpu_size_options"-->
<!--                                                            :key="item"-->
<!--                                                            :label="item"-->
<!--                                                            :value="item">-->
<!--                                                    </el-option>-->
<!--                                            </el-select>-->
<!--                                        </el-form-item>-->
<!--                                        <el-form-item label="软驱">-->
<!--                                            <el-select v-model="form.floppy_drive" placeholder="请选择软驱">-->
<!--                                                <el-option-->
<!--                                                        v-for="item in floppy_drive_options"-->
<!--                                                        :key="item"-->
<!--                                                        :label="item"-->
<!--                                                        :value="item">-->
<!--                                                </el-option>-->
<!--                                            </el-select>-->
<!--                                        </el-form-item>-->
                                    </el-tab-pane>
                                    <el-tab-pane label="选项" name="1">
                                        <el-row>
                                            <el-col :span="20">系统</el-col>
                                            <el-col :span="4"><el-button @click="handleRestoreDefault">恢复默认值</el-button></el-col>
                                        </el-row>
                                        <el-divider class="horizontal"></el-divider>
                                        <el-form-item label="时钟策略：" label-width="135px">
                                            <el-checkbox v-model="form.vmConfig.properties.clockMode">与主机时钟同步</el-checkbox>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">取消此选项，用户可自行设置虚拟机的时<br/>间，站点下所有主机时间必须同步，否则<br/>可能因主机时间不同步导致虚拟机HA、<br/>迁移、休眠唤醒、快照恢复虚拟机后时间<br/>发生跳变。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="启动引导固件：" label-width="135px">
                                            <el-radio-group v-model="form.vmConfig.properties.bootFirmware" @change="handleSelectBootFirmware">
                                                <el-radio :label="'BIOS'">BIOS</el-radio>
                                                <el-radio :label="'UEFI'">UEFI</el-radio>
                                            </el-radio-group>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">UEFI可扩展固件接口(Unified Extensible<br/> Firmware Interface)是传统BIOS的继任<br/>者，兼容MBR和GPT分区格式从而支持<br/>2T以上系统盘，但需要相应的操作系统支<br/>持，支持的操作系统类型详情请查看联机<br/>帮助。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="延迟时间(ms)：" label-width="135px">
                                            <el-input v-model="form.vmConfig.properties.bootFirmwareTime" :disabled="firmware_time_disabled" class="create-input" style="width: 200px;"></el-input>
                                        </el-form-item>
                                        <el-form-item label="启动方式：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.bootOption" placeholder="请选择启动方式" style="width: 200px;">
                                                <el-option
                                                        v-for="item in boot_mode_options"
                                                        :key="item.value"
                                                        :label="item.name"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="VNC键盘配置：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.vmVncKeymapSetting" placeholder="请选择VNC键盘配置" style="width: 200px;">
                                                <el-option
                                                        v-for="item in vnc_keyboard_options"
                                                        :key="item.id"
                                                        :label="item.vncKeymapDesCh"
                                                        :value="item.id">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="EVS亲和：" label-width="135px">
                                            <el-checkbox v-model="form.vmConfig.properties.evsAffinity">开启</el-checkbox>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">虚拟机EVS亲和开关开启、大页规格为1G<br/>且运行主机已配置用户态EVS时亲和性策<br/>略才生效，EVS亲和虚拟机CPU、内存与<br/>EVS转发核在同一物理NUMA节点分配。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="安全虚拟机：" label-width="135px">
                                            <el-switch
                                                    v-model="svm"
                                                    active-color="#13ce66"
                                                    @change="handleSwitchSvm">
                                            </el-switch>
                                        </el-form-item>
                                        <el-form-item v-if="svm" label="安全类型：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.safeType" @change="handleSwitchSecureVm" placeholder="请选择安全类型">
                                                <el-option
                                                        v-for="item in security_type_options"
                                                        :key="item.value"
                                                        :label="item.name"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item v-if="svm" label="安全虚拟机类型：" label-width="135px">
                                            <el-select v-model="secureVmTypeTo" placeholder="请选择安全虚拟机类型">
                                                <el-option
                                                        v-for="item in vm_security_type_options"
                                                        :key="item"
                                                        :label="item"
                                                        :value="item">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
<!--                                        <el-form-item label="NUMA结构自动调整：" label-width="160px">-->
<!--                                            <el-switch-->
<!--                                                    v-model="form.numa"-->
<!--                                                    active-color="#13ce66">-->
<!--                                            </el-switch>-->
<!--                                        </el-form-item>-->
                                    </el-tab-pane>
                                </el-tabs>
                            </el-row>
                            <el-row v-else-if="this.active===4" class="row_lineheight">
                                <el-row>
                                    <el-col :span="10"><div>创建类型：{{this.activeNameFormat(activeName)}}</div></el-col>
                                    <el-col :span="10"><div>虚拟机名称：{{form.name}}</div></el-col>
                                    <el-col :span="10"><div>描述：{{form.describtion}}</div></el-col>
                                    <el-col :span="10"><div>所在位置：{{parentObjUrnTo}}</div></el-col>
                                    <el-col :span="10"><div>计算资源：{{locationTo}}</div></el-col>
                                    <el-col :span="10"><div>是否与主机绑定：{{this.isBindingHostFormat(form.isBindingHost)}}</div></el-col>
                                    <el-col :span="10"><div>操作系统类型：{{form.osOptions.osType}}</div></el-col>
                                    <el-col :span="10"><div>操作系统版本号：{{this.osVersionFormat(form.osOptions.osVersion)}}</div></el-col>
                                </el-row>
                                <span style="font-size: 16px; font-weight: bold;">虚拟机配置</span>
                                <el-divider class="horizontal"></el-divider>
                                <el-row>
                                    <el-col :span="20"><div>CPU：{{form.vmConfig.cpu.quantity}}核</div></el-col>
<!--                                    <el-col :span="10"><div>CPU绑定：{{form.cpu_band}}</div></el-col>-->
<!--                                    <el-col :span="10"><div>CPU线程绑定策略：{{form.cpu_band_category}}</div></el-col>-->
                                    <el-col :span="10"><div>份额：{{form.vmConfig.cpu.weight}}</div></el-col>
                                    <el-col :span="10"><div>预留(MHz)：{{form.vmConfig.cpu.reservation}}</div></el-col>
                                    <el-col :span="10"><div>限制(MHz)：{{form.vmConfig.cpu.limit}}</div></el-col>
                                    <el-col :span="10"><div>插槽数：{{this.slotNumFormat(form.vmConfig.cpu.coresPerSocket)}}</div></el-col>
                                    <el-col :span="20"><div>每个插槽的内核数：{{form.vmConfig.cpu.coresPerSocket}}</div></el-col>
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>内存：{{form.vmConfig.memory.quantityMB}}GB</div></el-col>
                                    <el-col :span="10"><div>预留(MB)：{{form.vmConfig.memory.reservation}}</div></el-col>
                                    <el-col :span="10"><div>限制(MB)：{{form.vmConfig.memory.limit}}</div></el-col>
                                    <el-col :span="10"><div>份额：{{form.vmConfig.memory.weight}}</div></el-col>
<!--                                    <el-col :span="10"><div>大页配置：{{form.large_page_config}}</div></el-col>-->
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>磁盘1：{{form.vmConfig.disks[0].quantityGB}}GB</div></el-col>
                                    <el-col :span="10"><div>所属数据存储：{{form.vmConfig.disks[0].name}}</div></el-col>
                                    <el-col :span="10"><div>配置模式：{{form.vmConfig.disks[0].volType}}</div></el-col>
<!--                                    <el-col :span="10"><div>磁盘模式：{{form.disk_mode}}</div></el-col>-->
                                    <el-col :span="10"><div>总线类型：{{form.vmConfig.disks[0].pciType}}</div></el-col>
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>网卡1：{{this.portGroupUrnTo}}</div></el-col>
                                    <el-col :span="10"><div>网卡类型：{{form.vmConfig.nics[0].virtIo}}</div></el-col>
                                    <el-col :span="10"><div>IO环大小：{{form.vmConfig.nics[0].nicConfig.vringbuf}}</div></el-col>
                                    <el-col :span="10"><div>队列数：{{form.vmConfig.nics[0].nicConfig.queues}}</div></el-col>
                                    <el-col :span="10"><div>安全组：{{this.securityGroupFormat(form.vmConfig.nics[0].enableSecurityGroup)}}</div></el-col>
                                </el-row>
<!--                                <el-divider></el-divider>-->
<!--                                <el-row :gutter="20">-->
<!--                                    <el-col :span="20"><div>显卡：{{form.gpu}}</div></el-col>-->
<!--                                    <el-col :span="10"><div>显存(MB)：{{form.gpu_size}}</div></el-col>-->
<!--                                    <el-col :span="10"><div>设备类型：</div></el-col>-->
<!--                                </el-row>-->
<!--                                <el-divider></el-divider>-->
<!--                                <el-row :gutter="20">-->
<!--                                    <el-col :span="20"><div>软驱：{{form.floppy_drive}}</div></el-col>-->
<!--                                </el-row>-->
                                <el-divider></el-divider>
                                <el-row>
                                    <el-col :span="20">
                                        <span @click="showSystemInfo" style="color: #409eff;cursor: pointer">选项 {{arrow}}</span>
                                    </el-col>
                                </el-row>
                                <el-collapse-transition>
                                <div v-if="show_system">
                                    <span style="font-size: 16px; font-weight: bold;">系统</span>
                                    <el-divider class="horizontal"></el-divider>
                                    <el-row>
                                        <el-col :span="10"><div>时钟策略：{{this.clockModeFormat(form.vmConfig.properties.clockMode)}}</div></el-col>
                                        <el-col :span="10"><div>EVS亲和：{{this.evsAffinityFormat(form.vmConfig.properties.evsAffinity)}}</div></el-col>
                                        <el-col :span="10"><div>安全类型：{{this.safeTypeFormat(form.vmConfig.properties.safeType)}}</div></el-col>
                                        <el-col :span="10"><div>安全虚拟机类型：{{this.securiteTypeFormat(form.vmConfig.properties[form.vmConfig.properties.safeType])}}</div></el-col>
                                        <el-col :span="10"><div>启动引导固件：{{form.vmConfig.properties.bootFirmware}}</div></el-col>
                                        <el-col :span="10"><div>延迟时间(ms)：{{form.vmConfig.properties.bootFirmwareTime}}</div></el-col>
                                        <el-col :span="10"><div>VNC键盘配置：{{this.keymapSettingFormat(form.vmConfig.properties.vmVncKeymapSetting)}}</div></el-col>
                                        <el-col :span="10"><div>启动方式：{{this.bootOptionFormat(form.vmConfig.properties.bootOption)}}</div></el-col>
<!--                                        <el-col :span="20"><div>NUMA结构自动调整：{{form.numa}}</div></el-col>-->
                                    </el-row>
                                </div>
                                </el-collapse-transition>
                                <el-row>
                                    <el-col :span="6">
                                        <el-form-item labelWidth="0">
                                            <el-checkbox v-model="form.autoBoot" @click="handleAutoBoot">创建完成后直接启动虚拟机</el-checkbox>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-row>
                        </el-row>
                        <el-row v-if="this.activeName==='1'">
                            <el-row v-if="this.active===1">
                                <el-form-item label="名称：" prop="name" label-width="150px">
                                    <el-input v-model="form.name" class="create-input"></el-input>
                                </el-form-item>
                                <el-form-item label="描述：" prop="description" label-width="150px">
                                    <el-input type="textarea" v-model="form.descripttion" class="create-input"></el-input>
                                </el-form-item>
                                <el-form-item label="选择模板：" prop="vmsTemplate" label-width="150px">
                                    <el-input v-model="form.vmsTemplate" class="create-input" disabled></el-input>
                                    <el-button @click="handleSelectTemplate">选择</el-button>
                                </el-form-item>
                                <el-form-item label="选择虚拟机位置：" prop="parentObjUrn" label-width="150px">
                                    <el-input v-model="parentObjUrnTo" class="create-input" disabled></el-input>
                                    <el-button @click="handleSelectPosition">选择</el-button>
                                </el-form-item>
                                <el-form-item label="选择计算资源：" prop="location" label-width="150px">
                                    <el-input v-model="locationTo" class="create-input" disabled></el-input>
                                    <el-button @click="handleSelectCluster">选择</el-button>
                                    <el-checkbox v-model="form.isBindingHost" style="padding-left: 15px;" :disabled="checked_disabled">与所选主机绑定</el-checkbox>
                                </el-form-item>
                                <el-row :gutter="20">
                                    <el-col :span="11">
                                        <el-form-item label="虚拟机数量：" labelWidth="150px">
                                            <el-input-number v-model="form.vmSize" @change="handleAddVmSize" style="width: 130px;" :min="1" :max="50"></el-input-number>
                                        </el-form-item>
                                    </el-col>
                                    <el-col :span="11">
                                        <el-form-item label="名称后缀起始编号：" labelWidth="150px">
                                            <el-input-number v-model="form.namePostfixIndex" :disabled="postfix_index_disabled" style="width: 130px;" :min="0" :max="99999"></el-input-number>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-row>
                            <el-row v-else-if="this.active===2">
                                <el-tabs v-model="activeVMName" @tab-click="handleVMClick">
                                    <el-tab-pane label="硬件" name="0">
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showCPUInfo" :class="cpu_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="CPU" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.cpu.quantity" @change="handleCPUChange" style="width: 200px;" :min="1" :max="36"></el-input-number>
                                                    <el-tooltip class="item" effect="dark" placement="right">
                                                        <div slot="content">范围: 1-36<br/>建议虚拟机的内核数是每个插槽的内核数<br/>的整数倍。</div>
                                                        <i class="el-icon-warning bluecolor"></i>
                                                    </el-tooltip>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_cpu">
                                                        <!--                                                    <el-form-item label="CPU绑定" label-width="160px">-->
                                                        <!--                                                        <el-switch-->
                                                        <!--                                                                v-model="form.cpu_band"-->
                                                        <!--                                                                @change="handleBandCategory"-->
                                                        <!--                                                                active-color="#13ce66">-->
                                                        <!--                                                        </el-switch>-->
                                                        <!--                                                    </el-form-item>-->
                                                        <!--                                                    <el-form-item label="CPU线程绑定策略">-->
                                                        <!--                                                        <el-select :disabled="cpu_disabled" v-model="form.cpu_band_category" placeholder="请选择绑定策略">-->
                                                        <!--                                                            <el-option-->
                                                        <!--                                                                    v-for="item in cpu_band_category_options"-->
                                                        <!--                                                                    :key="item"-->
                                                        <!--                                                                    :label="item"-->
                                                        <!--                                                                    :value="item">-->
                                                        <!--                                                            </el-option>-->
                                                        <!--                                                        </el-select>-->
                                                        <!--                                                    </el-form-item>-->
                                                        <el-form-item label="份额" label-width="135px">
                                                            <el-select v-model="cpu_share" @change="handleCpuShare" placeholder="份额" style="width: 100px;">
                                                                <el-option
                                                                        v-for="item in cpu_share_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-input :disabled="cpu_share_disabled" v-model="form.vmConfig.cpu.weight" style="width: 100px;"></el-input>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">描述：定义多个虚拟机在竞争物理CPU资<br/>源时按比例分配，份额越高的虚拟机，竞<br/>争物理CPU时获取的资源越多。 <br/>范围：<br/>
                                                                    低：内核数*250<br/>
                                                                    中：内核数*500<br/>
                                                                    高：内核数*1000<br/>
                                                                    自定义：2~255000</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="每个插槽内核数" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.coresPerSocket" style="width: 200px;" :min="1" :max="36"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 1-36<br/>插槽数:{{Math.ceil(form.vmConfig.cpu.quantity/form.vmConfig.cpu.coresPerSocket)}}</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="预留(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.reservation" style="width: 200px;" :min="0" :max="4400"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 0-{{form.vmConfig.cpu.quantity*2200}}<br/>
                                                                    定义了多个虚拟机竞争物理CPU资源的时<br/>候分配的最低计算资源。如果指定CPU的<br/>预留值，需要排除故障和已经停止的主<br/>机。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="限制(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.cpu.limit" style="width: 200px;" :min="0" :max="4400"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">0表示不限<br/>
                                                                    控制虚拟机占用物理CPU资源的上限。以<br/>一个两CPU的虚拟机为例，如果设置该虚<br/>拟机CPU上限为3000MHz，则该虚拟机的<br/>两个虚拟CPU计算能力被限制为<br/>1500MHz。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showMemInfo" :class="mem_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="内存" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.memory.quantityMB" @change="handleMemChange" style="width: 200px;" :min="1" :max="4096"></el-input-number>
                                                    <el-button type="primary" style="margin-left: 5px;">GB</el-button>
                                                    <el-tooltip class="item" effect="dark" placement="right">
                                                        <div slot="content">32位系统无法充分利用4G内存，建议32<br/>位系统无需配满4G内存，可以配置<br/>3583MB内存（约3.5GB）。</div>
                                                        <i class="el-icon-warning" style="color:#66b1ff;"></i>
                                                    </el-tooltip>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_mem">
                                                        <!--                                                <el-form-item label="大页配置">-->
                                                        <!--                                                    <el-select v-model="form.large_page_config" @change="handleLargePageConfig" placeholder="大页配置">-->
                                                        <!--                                                        <el-option-->
                                                        <!--                                                                v-for="item in large_page_config_options"-->
                                                        <!--                                                                :key="item"-->
                                                        <!--                                                                :label="item"-->
                                                        <!--                                                                :value="item">-->
                                                        <!--                                                        </el-option>-->
                                                        <!--                                                    </el-select>-->
                                                        <!--                                                </el-form-item>-->
                                                        <el-form-item label="份额" label-width="135px">
                                                            <el-select v-model="mem_share" @change="handleMemShare" placeholder="份额" style="width: 100px;">
                                                                <el-option
                                                                        v-for="item in cpu_share_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-input v-model="form.vmConfig.memory.weight" :disabled="mem_share_disabled" class="create-input" style="width: 100px;"></el-input>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">低：内存大小 * 5<br/>
                                                                    中：内存大小 * 10<br/>
                                                                    高：内存大小 * 20<br/>
                                                                    自定义：1~83886080</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="预留(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.memory.reservation" :disabled="mem_reserve_disabled" style="width: 200px;" :min="0" :max="4096"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: 0-{{form.vmConfig.memory.quantityMB*1024}}<br/>
                                                                    当集群的内存复用开启时,内存预留值生<br/>效;<br/>
                                                                    具有PCI直通设备(包括SRIOV)的虚拟机<br/>或是虚拟机所在主机配置了内存盘模式，<br/>内存预留值必须和内存规格值相等，即必<br/>须全预留。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="限制(MHz)" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.memory.limit" :disabled="mem_limit_disabled" style="width: 200px;" :min="0" :max="4096"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">范围: {{form.vmConfig.memory.quantityMB*1024}}-{{form.vmConfig.memory.quantityMB*1024}}, 0表示不限</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showDiskInfo" :class="disk_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="磁盘1" label-width="135px">
                                                    <el-input-number v-model="form.vmConfig.disks[0].quantityGB" disabled @change="handleCPUChange" style="width: 200px;" :min="1" :max="1024"></el-input-number>
                                                    <el-button type="primary" style="margin-left: 5px;">GB</el-button>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_disk">
                                                        <el-form-item label="数据存储" prop="dataStore" label-width="135px">
                                                            <el-input v-model="form.vmConfig.disks[0].name" style="width: 150px;" disabled></el-input>
                                                            <el-button @click="handleSelectDataStore">选择</el-button>
                                                        </el-form-item>
                                                        <el-form-item label="配置模式" label-width="135px">
                                                            <el-select v-model="form.vmConfig.disks[0].volType" @change="handleSelectVolType" placeholder="配置模式">
                                                                <el-option
                                                                        v-for="item in config_mode_options"
                                                                        :key="item.value"
                                                                        :label="item.name"
                                                                        :value="item.value">
                                                                </el-option>
                                                            </el-select>
                                                        </el-form-item>
                                                        <!--                                                <el-form-item label="磁盘模式">-->
                                                        <!--                                                    <el-select v-model="form.disk_mode" placeholder="磁盘模式" style="width: 200px;">-->
                                                        <!--                                                        <el-option-->
                                                        <!--                                                                v-for="item in disk_mode_options"-->
                                                        <!--                                                                :key="item"-->
                                                        <!--                                                                :label="item"-->
                                                        <!--                                                                :value="item">-->
                                                        <!--                                                        </el-option>-->
                                                        <!--                                                    </el-select>-->
                                                        <!--                                                </el-form-item>-->
                                                        <el-form-item label="总线类型" label-width="135px">
                                                            <el-select v-model="form.vmConfig.disks[0].pciType" placeholder="总线类型">
                                                                <el-option
                                                                        v-for="item in bus_type_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">VIRTIO/IDE/SCSI :创建虚拟机时，数据<br/>存储上创建的磁盘可以挂载在VIRTIO、<br/>IDE、SCSI总线上，VIRTIO性能较好，<br/>IDE性能较差，仅用于虚拟机镜像制作及<br/>虚拟机光驱。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <el-row>
                                            <el-col :span="2" class="mt10">
                                                <span @click="showNetworkInfo" :class="network_arrow_icon"></span>
                                            </el-col>
                                            <el-col :span="22">
                                                <el-form-item label="网卡1" label-width="135px">
                                                    <el-input v-model="portGroupUrnTo" style="width: 150px;" disabled></el-input>
                                                    <el-button @click="handleNetworkSwitch">选择</el-button>
                                                </el-form-item>
                                                <el-collapse-transition>
                                                    <div v-if="show_network">
                                                        <el-form-item label="网卡类型" label-width="135px">
                                                            <el-select v-model="form.vmConfig.nics[0].virtIo" placeholder="网卡类型">
                                                                <el-option
                                                                        v-for="item in network_type_options"
                                                                        :key="item.value"
                                                                        :label="item.name"
                                                                        :value="item.value">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">virtio : 高网络吞吐量和降低网络延迟的网<br/>卡类型。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="IO环大小" label-width="135px">
                                                            <el-select v-model="form.vmConfig.nics[0].nicConfig.vringbuf" placeholder="IO环大小">
                                                                <el-option
                                                                        v-for="item in IO_ring_num_options"
                                                                        :key="item"
                                                                        :label="item"
                                                                        :value="item">
                                                                </el-option>
                                                            </el-select>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">通过适当的调大IO环，可以缓解前端驱动<br/>的丢包，提高性能。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="队列数" label-width="135px">
                                                            <el-input-number v-model="form.vmConfig.nics[0].nicConfig.queues" @change="handleCPUChange" style="width: 210px;" :min="1" :max="form.vmConfig.cpu.quantity"></el-input-number>
                                                            <el-tooltip class="item" effect="dark" placement="right">
                                                                <div slot="content">队列数取值不能超过虚拟机当前的vCPU<br/>数量。</div>
                                                                <i class="el-icon-warning bluecolor"></i>
                                                            </el-tooltip>
                                                        </el-form-item>
                                                        <el-form-item label="开启安全组" label-width="135px">
                                                            <el-switch
                                                                    v-model="form.vmConfig.nics[0].enableSecurityGroup"
                                                                    active-color="#13ce66"
                                                                    @change="handleSwitchSecurityGroup">
                                                            </el-switch>
                                                        </el-form-item>
                                                        <el-form-item v-if="form.vmConfig.nics[0].enableSecurityGroup" label="安全组" label-width="135px">
                                                            <el-input v-model="form.vmConfig.nics[0].securityGroupId" style="width: 150px;"></el-input>
                                                            <el-button @click="handleSelectSecurityGroup">选择</el-button>
                                                        </el-form-item>
                                                    </div>
                                                </el-collapse-transition>
                                            </el-col>
                                        </el-row>
                                        <!--                                        <el-form-item label="显卡">-->
                                        <!--                                            <el-select v-model="form.gpu" @change="handleSelectGpuSize" placeholder="请选择显卡" style="width: 100px;">-->
                                        <!--                                                <el-option-->
                                        <!--                                                        v-for="item in gpu_options"-->
                                        <!--                                                        :key="item"-->
                                        <!--                                                        :label="item"-->
                                        <!--                                                        :value="item">-->
                                        <!--                                                </el-option>-->
                                        <!--                                            </el-select>-->
                                        <!--                                            <el-select v-model="form.gpu_size" placeholder="请选择显卡大小" style="width: 100px; padding-left: 10px;">-->
                                        <!--                                                    <el-option-->
                                        <!--                                                            v-for="item in gpu_size_options"-->
                                        <!--                                                            :key="item"-->
                                        <!--                                                            :label="item"-->
                                        <!--                                                            :value="item">-->
                                        <!--                                                    </el-option>-->
                                        <!--                                            </el-select>-->
                                        <!--                                        </el-form-item>-->
                                        <!--                                        <el-form-item label="软驱">-->
                                        <!--                                            <el-select v-model="form.floppy_drive" placeholder="请选择软驱">-->
                                        <!--                                                <el-option-->
                                        <!--                                                        v-for="item in floppy_drive_options"-->
                                        <!--                                                        :key="item"-->
                                        <!--                                                        :label="item"-->
                                        <!--                                                        :value="item">-->
                                        <!--                                                </el-option>-->
                                        <!--                                            </el-select>-->
                                        <!--                                        </el-form-item>-->
                                    </el-tab-pane>
                                    <el-tab-pane label="选项" name="1">
                                        <el-row>
                                            <el-col :span="20">系统</el-col>
                                            <el-col :span="4"><el-button @click="handleRestoreDefault">恢复默认值</el-button></el-col>
                                        </el-row>
                                        <el-divider class="horizontal"></el-divider>
                                        <el-form-item label="时钟策略：" label-width="135px">
                                            <el-checkbox v-model="form.vmConfig.properties.clockMode">与主机时钟同步</el-checkbox>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">取消此选项，用户可自行设置虚拟机的时<br/>间，站点下所有主机时间必须同步，否则<br/>可能因主机时间不同步导致虚拟机HA、<br/>迁移、休眠唤醒、快照恢复虚拟机后时间<br/>发生跳变。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="启动引导固件：" label-width="135px">
                                            <el-radio-group v-model="form.vmConfig.properties.bootFirmware" disabled @change="handleSelectBootFirmware">
                                                <el-radio :label="'BIOS'">BIOS</el-radio>
                                                <el-radio :label="'UEFI'">UEFI</el-radio>
                                            </el-radio-group>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">UEFI可扩展固件接口(Unified Extensible<br/> Firmware Interface)是传统BIOS的继任<br/>者，兼容MBR和GPT分区格式从而支持<br/>2T以上系统盘，但需要相应的操作系统支<br/>持，支持的操作系统类型详情请查看联机<br/>帮助。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="延迟时间(ms)：" label-width="135px">
                                            <el-input v-model="form.vmConfig.properties.bootFirmwareTime" :disabled="firmware_time_disabled" class="create-input" style="width: 200px;"></el-input>
                                        </el-form-item>
                                        <el-form-item label="启动方式：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.bootOption" placeholder="请选择启动方式" style="width: 200px;">
                                                <el-option
                                                        v-for="item in boot_mode_options"
                                                        :key="item.value"
                                                        :label="item.name"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="VNC键盘配置：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.vmVncKeymapSetting" placeholder="请选择VNC键盘配置" style="width: 200px;">
                                                <el-option
                                                        v-for="item in vnc_keyboard_options"
                                                        :key="item.id"
                                                        :label="item.vncKeymapDesCh"
                                                        :value="item.id">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item label="EVS亲和：" label-width="135px">
                                            <el-checkbox v-model="form.vmConfig.properties.evsAffinity">开启</el-checkbox>
                                            <el-tooltip class="item" effect="dark" placement="right">
                                                <div slot="content">虚拟机EVS亲和开关开启、大页规格为1G<br/>且运行主机已配置用户态EVS时亲和性策<br/>略才生效，EVS亲和虚拟机CPU、内存与<br/>EVS转发核在同一物理NUMA节点分配。</div>
                                                <i class="el-icon-warning bluecolor"></i>
                                            </el-tooltip>
                                        </el-form-item>
                                        <el-form-item label="安全虚拟机：" label-width="135px">
                                            <el-switch
                                                    v-model="svm"
                                                    active-color="#13ce66"
                                                    @change="handleSwitchSvm">
                                            </el-switch>
                                        </el-form-item>
                                        <el-form-item v-if="svm" label="安全类型：" label-width="135px">
                                            <el-select v-model="form.vmConfig.properties.safeType" @change="handleSwitchSecureVm" placeholder="请选择安全类型">
                                                <el-option
                                                        v-for="item in security_type_options"
                                                        :key="item.value"
                                                        :label="item.name"
                                                        :value="item.value">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <el-form-item v-if="svm" label="安全虚拟机类型：" label-width="135px">
                                            <el-select v-model="secureVmTypeTo" placeholder="请选择安全虚拟机类型">
                                                <el-option
                                                        v-for="item in vm_security_type_options"
                                                        :key="item"
                                                        :label="item"
                                                        :value="item">
                                                </el-option>
                                            </el-select>
                                        </el-form-item>
                                        <!--                                        <el-form-item label="NUMA结构自动调整：" label-width="160px">-->
                                        <!--                                            <el-switch-->
                                        <!--                                                    v-model="form.numa"-->
                                        <!--                                                    active-color="#13ce66">-->
                                        <!--                                            </el-switch>-->
                                        <!--                                        </el-form-item>-->
                                    </el-tab-pane>
                                </el-tabs>
                            </el-row>
                            <el-row v-else-if="this.active===3">
                                <el-row>
                                    <el-col :span="10"><div>创建类型：{{this.activeNameFormat(activeName)}}</div></el-col>
                                    <el-col :span="10"><div>虚拟机名称：{{form.name}}</div></el-col>
                                    <el-col :span="10"><div>描述：{{form.describtion}}</div></el-col>
                                    <el-col :span="10"><div>所在位置：{{parentObjUrnTo}}</div></el-col>
                                    <el-col :span="10"><div>计算资源：{{locationTo}}</div></el-col>
                                    <el-col :span="10"><div>是否与主机绑定：{{this.isBindingHostFormat(form.isBindingHost)}}</div></el-col>
                                    <el-col :span="10"><div>操作系统类型：{{form.osOptions.osType}}</div></el-col>
                                    <el-col :span="10"><div>操作系统版本号：{{this.osVersionFormat(form.osOptions.osVersion)}}</div></el-col>
                                </el-row>
                                <span style="font-size: 16px; font-weight: bold;">虚拟机配置</span>
                                <el-divider class="horizontal"></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>CPU：{{form.vmConfig.cpu.quantity}}核</div></el-col>
                                    <!--                                    <el-col :span="10"><div>CPU绑定：{{form.cpu_band}}</div></el-col>-->
                                    <!--                                    <el-col :span="10"><div>CPU线程绑定策略：{{form.cpu_band_category}}</div></el-col>-->
                                    <el-col :span="10"><div>份额：{{form.vmConfig.cpu.weight}}</div></el-col>
                                    <el-col :span="10"><div>预留(MHz)：{{form.vmConfig.cpu.reservation}}</div></el-col>
                                    <el-col :span="10"><div>限制(MHz)：{{form.vmConfig.cpu.limit}}</div></el-col>
                                    <el-col :span="10"><div>插槽数：{{this.slotNumFormat(form.vmConfig.cpu.coresPerSocket)}}</div></el-col>
                                    <el-col :span="20"><div>每个插槽的内核数：{{form.vmConfig.cpu.coresPerSocket}}</div></el-col>
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>内存：{{form.vmConfig.memory.quantityMB}}GB</div></el-col>
                                    <el-col :span="10"><div>预留(MB)：{{form.vmConfig.memory.reservation}}</div></el-col>
                                    <el-col :span="10"><div>限制(MB)：{{form.vmConfig.memory.limit}}</div></el-col>
                                    <el-col :span="10"><div>份额：{{form.vmConfig.memory.weight}}</div></el-col>
                                    <!--                                    <el-col :span="10"><div>大页配置：{{form.large_page_config}}</div></el-col>-->
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>磁盘1：{{form.vmConfig.disks[0].quantityGB}}GB</div></el-col>
                                    <el-col :span="10"><div>所属数据存储：{{form.vmConfig.disks[0].name}}</div></el-col>
                                    <el-col :span="10"><div>配置模式：{{form.vmConfig.disks[0].volType}}</div></el-col>
                                    <!--                                    <el-col :span="10"><div>磁盘模式：{{form.disk_mode}}</div></el-col>-->
                                    <el-col :span="10"><div>总线类型：{{form.vmConfig.disks[0].pciType}}</div></el-col>
                                </el-row>
                                <el-divider></el-divider>
                                <el-row >
                                    <el-col :span="20"><div>网卡1：{{this.portGroupUrnTo}}</div></el-col>
                                    <el-col :span="10"><div>网卡类型：{{form.vmConfig.nics[0].virtIo}}</div></el-col>
                                    <el-col :span="10"><div>IO环大小：{{form.vmConfig.nics[0].nicConfig.vringbuf}}</div></el-col>
                                    <el-col :span="10"><div>队列数：{{form.vmConfig.nics[0].nicConfig.queues}}</div></el-col>
                                    <el-col :span="10"><div>安全组：{{this.securityGroupFormat(form.vmConfig.nics[0].enableSecurityGroup)}}</div></el-col>
                                </el-row>
                                <!--                                <el-divider></el-divider>-->
                                <!--                                <el-row :gutter="20">-->
                                <!--                                    <el-col :span="20"><div>显卡：{{form.gpu}}</div></el-col>-->
                                <!--                                    <el-col :span="10"><div>显存(MB)：{{form.gpu_size}}</div></el-col>-->
                                <!--                                    <el-col :span="10"><div>设备类型：</div></el-col>-->
                                <!--                                </el-row>-->
                                <!--                                <el-divider></el-divider>-->
                                <!--                                <el-row :gutter="20">-->
                                <!--                                    <el-col :span="20"><div>软驱：{{form.floppy_drive}}</div></el-col>-->
                                <!--                                </el-row>-->
                                <el-divider></el-divider>
                                <el-row>
                                    <el-col :span="20">
                                        <span @click="showSystemInfo" style="color: #409eff;">选项 {{arrow}}</span>
                                    </el-col>
                                </el-row>
                                <el-collapse-transition>
                                    <div v-if="show_system">
                                        <span style="font-size: 16px; font-weight: bold;">系统</span>
                                        <el-divider class="horizontal"></el-divider>
                                        <el-row>
                                            <el-col :span="10"><div>时钟策略：{{this.clockModeFormat(form.vmConfig.properties.clockMode)}}</div></el-col>
                                            <el-col :span="10"><div>EVS亲和：{{this.evsAffinityFormat(form.vmConfig.properties.evsAffinity)}}</div></el-col>
                                            <el-col :span="10"><div>安全类型：{{this.safeTypeFormat(form.vmConfig.properties.safeType)}}</div></el-col>
                                            <el-col :span="10"><div>安全虚拟机类型：{{this.securiteTypeFormat(form.vmConfig.properties[form.vmConfig.properties.safeType])}}</div></el-col>
                                            <el-col :span="10"><div>启动引导固件：{{form.vmConfig.properties.bootFirmware}}</div></el-col>
                                            <el-col :span="10"><div>延迟时间(ms)：{{form.vmConfig.properties.bootFirmwareTime}}</div></el-col>
                                            <el-col :span="10"><div>VNC键盘配置：{{this.keymapSettingFormat(form.vmConfig.properties.vmVncKeymapSetting)}}</div></el-col>
                                            <el-col :span="10"><div>启动方式：{{this.bootOptionFormat(form.vmConfig.properties.bootOption)}}</div></el-col>
                                            <!--                                        <el-col :span="20"><div>NUMA结构自动调整：{{form.numa}}</div></el-col>-->
                                        </el-row>
                                    </div>
                                </el-collapse-transition>
                                <el-row>
                                    <el-col :span="6">
                                        <el-form-item labelWidth="0">
                                            <el-checkbox v-model="form.autoBoot" @click="handleAutoBoot">创建完成后直接启动虚拟机</el-checkbox>
                                        </el-form-item>
                                    </el-col>
                                </el-row>
                            </el-row>
                        </el-row>
                        </div>
                    </el-col>
                </el-row>
                </el-form>
            </div>
                <span slot="footer" class="dialog-footer">
                    <el-button @click="prevStep" :disabled="prev_disabled">上一步</el-button>
                    <el-button type="primary" @click="nextStep">{{next_step}}</el-button>
                </span>
        </el-dialog>
        <!-- 虚拟机位置选择弹出框 -->
        <el-dialog title="选择虚拟机位置" :visible.sync="positionVisible" width="38%">
            <div class="selecct-dialog-div">
                <el-tree
                        :data="position_data"
                        highlight-current
                        :expand-on-click-node="false"
                        :props="defaultProps"
                        @node-click="handlePositionClick"> <!-- default-expand-all -->
                    <span class="custom-tree-node" slot-scope="{ node }">
                        <span>
                            <i style="font-size: 10px;" class="el-icon-caret-bottom"></i> {{ node.label }}
                        </span>
                    </span>
                </el-tree>
            </div>
            <span slot="footer" class="dialog-footer">
                    <el-button @click="cancelPosition">取 消</el-button>
                    <el-button type="primary" @click="addPosition">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 计算资源选择弹出框 -->
        <el-dialog title="选择计算资源" :visible.sync="clusterVisible" width="38%">
            <div class="select-dialog-div">
                <el-tree
                        :load="loadNode"
                        :expand-on-click-node="false"
                        default-expand-all
                        highlight-current
                        :props="defaultProps"
                        lazy
                        @node-click="handleClusterClick"
                ></el-tree>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelCluster">取 消</el-button>
                <el-button type="primary" @click="addCluster">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 虚拟机模板选择弹出框 -->
        <el-dialog title="选择模板" :visible.sync="templateVisible" width="65%">
            <div class="vm-dialog-div">
                <el-table
                        :data="templateTableData"
                        border
                        style="width:100%"
                        highlight-current-row
                        max-height="600"
                        @current-change="handleTemplateChange"
                >
                    <el-table-column prop="name" label="名称" align="center"></el-table-column>
                    <el-table-column prop="uri" :formatter="uriFormat" label="ID" align="center"></el-table-column>
                    <el-table-column prop="status" :formatter="statusFormat" label="状态" align="center"></el-table-column>
                    <el-table-column prop="clusterName" label="所在集群" align="center"></el-table-column>
                    <el-table-column prop="hostName" label="所在主机" align="center"></el-table-column>
                    <el-table-column prop="isBindingHost" :formatter="isBindingFormat" label="与主机绑定" align="center"></el-table-column>
                </el-table>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelTemplate">取 消</el-button>
                <el-button type="primary" @click="addTemplate">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 磁盘选择数据存储弹出框 -->
        <el-dialog title="选择数据存储" :visible.sync="dataStoreVisible" width="65%">
            <div class="vm-dialog-div">
                <el-table
                        :data="storeTableData"
                        border
                        style="width:100%"
                        highlight-current-row
                        max-height="600"
                        @current-change="handleDataStoreChange"
                >
                    <el-table-column prop="name" label="名称" align="center"></el-table-column>
                    <el-table-column prop="actualFreeSizeGB" label="可用容量(GB)" align="center"></el-table-column>
                    <el-table-column prop="usedSizeGB" label="已分配容量(GB)" align="center"></el-table-column>
                    <el-table-column prop="capacityGB" label="总容量(GB)" align="center"></el-table-column>
                    <el-table-column prop="isThin" :formatter="storageisThinFormat" label="精简配置" align="center"></el-table-column>
                    <el-table-column prop="storageType" :formatter="storageTypeFormat" label="类型" align="center"></el-table-column>
                    <el-table-column prop="dsLockType" :formatter="storageLockTypeFormat" label="锁类型" align="center"></el-table-column>
                    <el-table-column prop="refreshTime" label="上次更新时间" align="center"></el-table-column>
                </el-table>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelDataStore">取 消</el-button>
                <el-button type="primary" @click="addDataStore">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 网卡选择交换机弹出框 -->
        <el-dialog title="选择端口组" :visible.sync="networkSwitchVisible" width="55%">
            <div class="select-dialog-div">
                <span>分布式交换机：</span>
                <el-select v-model="form.dv_switch" @change="handleSetPortGroupNum" placeholder="请选择分布式交换机">
                    <el-option
                            v-for="item in dv_switch_options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value">
                    </el-option>
                </el-select>
                <el-table
                        :data="portGroupTableData"
                        border
                        style="width:100%"
                        highlight-current-row
                        max-height="600"
                        @current-change="handlePortGroupChange"
                >
                    <el-table-column prop="name" label="端口组名称" align="center"></el-table-column>
                    <el-table-column prop="portType" :formatter="portTypeFormat" label="端口类型" align="center"></el-table-column>
<!--                    <el-table-column prop="userType" label="连接方式" align="center"></el-table-column>-->
                    <el-table-column prop="vlanId" label="VLAN" align="center"></el-table-column>
                </el-table>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelPortGroup">取 消</el-button>
                <el-button type="primary" @click="addPortGroup">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 网卡选择安全组弹出框 -->
        <el-dialog title="选择安全组" :visible.sync="securityGroupVisible" width="45%">
            <div class="vm-dialog-div">
                <el-table
                        :data="securityGroupTableData"
                        border
                        style="width:100%"
                        highlight-current-row
                        max-height="600"
                        @current-change="handleSecurityGroupChange"
                >
                    <el-table-column prop="sgName" label="名称" align="center"></el-table-column>
                    <el-table-column prop="sgId" label="安全组ID" align="center"></el-table-column>
                    <el-table-column prop="rules" label="规则数量" align="center"></el-table-column>
                    <el-table-column prop="description" label="描述" align="center"></el-table-column>
                </el-table>
            </div>
            <span slot="footer" class="dialog-footer">
                <el-button @click="cancelSecurityGroup">取 消</el-button>
                <el-button type="primary" @click="addSecurityGroup">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 删除弹出框 -->
        <el-dialog title="提示" :visible.sync="deleteVisible" width="25%">
            <span>确定要删除虚拟机 {{vms_name}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="deleteVisible = false">取 消</el-button>
                <el-button type="primary" @click="deleteVms">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 停止虚拟机弹出框 -->
        <el-dialog title="提示" :visible.sync="stopVisible" width="25%">
            <span>确定要停止虚拟机 {{vms_name}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="stopVisible = false">取 消</el-button>
                <el-button type="primary" @click="stopVms">确 定</el-button>
            </span>
        </el-dialog>
        <!-- 开启虚拟机弹出框 -->
        <el-dialog title="提示" :visible.sync="startVisible" width="25%">
            <span>确定要运行虚拟机 {{vms_name}} 吗？</span>
            <span slot="footer" class="dialog-footer">
                <el-button @click="startVisible = false">取 消</el-button>
                <el-button type="primary" @click="startVms">确 定</el-button>
            </span>
        </el-dialog>
    </div>
</template>

<script>
    // import Editor from 'vue2-ace-editor'
    export default {
        data() {
            return {
                options: [],
                step_options: [
                    {
                        value: '选项1',
                        label: '选择创建类型'
                    }, {
                        value: '选项2',
                        label: '基本配置'
                    }, {
                        value: '选项3',
                        label: '选择数据存储'
                    }, {
                        value: '选项4',
                        label: '虚拟机配置'
                    }, {
                        value: '选项5',
                        label: '确认信息'
                    }
                ],
                os_type_arr: [
                    {id: 1, label: 'Windows'},
                    {id: 2, label: 'Linux'},
                    {id: 3, label: '其他'}
                ],
                position_data: [],
                cluster_data: [],
                host_data: [],
                defaultProps: {
                    children: 'children',
                    label: 'label'
                },
                huaweiyun_options: [],
                os_version_options: [],
                gpu_options: ['VGA'],
                floppy_drive_options: ['自动匹配'],
                gpu_size_options: [],
                security_type_options: [],
                vm_security_type_options: [],
                cpu_band_category_options: [],
                cpu_share_options: [],
                large_page_config_options: [],
                config_mode_options: [],
                disk_mode_options: [],
                bus_type_options: [],
                network_type_options: [],
                IO_ring_num_options: [],
                dv_switch_options: [],
                boot_mode_options: [],
                vnc_keyboard_options: [],
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                keywords: '',
                tableData: [],
                storeTableData: [],
                templateTableData: [],
                portGroupTableData: [],
                securityGroupTableData: [],
                multipleSelection: [],
                delList: [],
                title: '',
                editVisible: false,
                deleteVisible: false,
                stopVisible: false,
                startVisible: false,
                positionVisible: false,
                templateVisible: false,
                clusterVisible: false,
                dataStoreVisible: false,
                networkSwitchVisible: false,
                securityGroupVisible: false,
                datetimeFormat: null,
                pageTotal: 0,
                huaweiyun_env: '',
                huaweiyun_env_info: '',
                select_vm_position: '',
                select_vm_cluster: '',
                select_vm_cluster_to: '',
                currentSelectDataStore: '',
                currentSelectPortGroup: '',
                currentSelectSecurityGroup: '',
                currentSelectDataStoreUrn: '',
                currentSelectTemplate: '',
                show_system: false,
                show_cpu: false,
                show_mem: false,
                show_network: false,
                show_disk: false,
                prev_disabled: true,
                checked_disabled: true,
                cpu_disabled: true,
                cpu_share_disabled: true,
                mem_share_disabled: true,
                mem_reserve_disabled: false,
                mem_limit_disabled: false,
                firmware_time_disabled: false,
                postfix_index_disabled: true,
                svm: false,
                next_step: '下一步',
                arrow: '>>',
                cpu_arrow_icon: 'el-icon-caret-right',
                mem_arrow_icon: 'el-icon-caret-right',
                disk_arrow_icon: 'el-icon-caret-right',
                network_arrow_icon: 'el-icon-caret-right',
                select_level: 0,
                form: {
                    name: '',
                    description: '',
                    parentObjUrn: '',
                    location: '',
                    osOptions: {
                        osType: 'Windows',
                        osVersion: '',
                    },
                    vmConfig: {
                        cpu: {
                            weight: 1000,
                            reservation: 0,
                            quantity: 2,
                            limit: 0,
                            coresPerSocket: 1
                        },
                        memory: {
                            quantityMB: 4,
                            reservation: 0,
                            weight: 40960,
                            limit: 0
                        },
                        disks: [{
                            datastoreUrn: "",
                            name: "autoDS_CNA001",
                            quantityGB: 40,
                            sequenceNum: 1,
                            isThin: false,
                            pciType: "VIRTIO",
                            volType: 1,
                        }],
                        nics: [{
                            sequenceNum: 0,
                            portGroupUrn: "",
                            virtIo: 1,
                            nicConfig: {
                                vringbuf: 256,
                                queues: 1
                            },
                            enableSecurityGroup: false,
                        }],
                        properties: {
                            clockMode: false,
                            bootFirmware: "BIOS",
                            evsAffinity: false,
                            bootFirmwareTime: 0,
                            bootOption: "disk",
                            vmVncKeymapSetting: 7,
                            isAutoAdjustNuma: false,
                        }
                        },
                    isBindingHost: false,
                    autoBoot: true,
                },
                idx: -1,
                id: -1,
                activeName: '0',
                activeVMName: '0',
                active: 0,
                showOption:false,
                locationTo: '',
                parentObjUrnTo: '',
                portGroupUrnTo: '',
                secureVmTypeTo: "GVM",
                vms_name: '',
                cpu_share: '中',
                mem_share: '中',
                template_id: '',
                loading: true,
                rules: {
                    name: [
                        { required: true, message: '请输入虚拟机名称' }
                    ],
                    parentObjUrn: [
                        { required: true, message: '请选择虚拟机位置', trigger: 'blur' }
                    ],
                    location: [
                        { required: true, message: '请选择计算资源', trigger: 'change' }
                    ],
                    vmsTemplate: [
                        { required: true, message: '请选择虚拟机模板', trigger: 'change' }
                    ]
                },
            };

        },
        created() {
            this.token =  localStorage.getItem('token');
            this.username = localStorage.getItem('username');
            this.getHuaweiyunData();
        },
        methods: {
            // 格式化创建类型
            activeNameFormat(activeName) {
              if(activeName==='0') {
                  return '创建新虚拟机'
              }else if(activeName==='1') {
                  return '使用模板部署虚拟机'
              }
            },
            // 格式化插槽数
            slotNumFormat(core_num) {
                if(core_num===1) {
                    return this.form.vmConfig.cpu.quantity;
                }else {
                    return Math.ceil(this.form.vmConfig.cpu.quantity/core_num);
                }
            },
            // 格式化绑定状态
            isBindingFormat(row) {
                if(row.isBindingHost===false) {
                    return '否'
                }else {
                    return '是'
                }
            },
            // 格式化模板ID
            uriFormat(row) {
                return row.uri.split("/")[5];
            },
            // 格式化主机绑定
            isBindingHostFormat(isBind) {
                if(isBind===false) {
                    return '不绑定'
                }else {
                    return '绑定'
                }
            },
            // 格式化操作系统版本
            osVersionFormat(osVersion) {
                for(let i = 0; i < this.os_version_options.length; i++){
                    if(this.os_version_options[i].os_id===osVersion){
                        return this.os_version_options[i].os_version;
                    }
                }
            },
            // 格式化安全组
            securityGroupFormat(securityGroup) {
                if(securityGroup===false) {
                    return '未开启'
                }else {
                    return this.form.vmConfig.nics[0].securityGroupId
                }
            },
            // 格式化evs亲和
            evsAffinityFormat(evsAffinity) {
                if(evsAffinity===false) {
                    return '未开启'
                }else {
                    return '开启'
                }
            },
            // 格式化时钟类型
            clockModeFormat(clockMode) {
                if(clockMode===false) {
                    return '自由时钟'
                }else {
                    return '同步时钟'
                }
            },
            // 格式化键盘配置
            keymapSettingFormat(keymapSetting) {
                if(keymapSetting===7) {
                    return '英语（美国）'
                }else if(keymapSetting===12) {
                    return '法语'
                }else if(keymapSetting===4) {
                    return '德语'
                }else if(keymapSetting===19) {
                    return '意大利语'
                }else if(keymapSetting===30) {
                    return '俄语'
                }else if(keymapSetting===8) {
                    return '西班牙语'
                }
            },
            // 格式化启动方式
            bootOptionFormat(bootOption) {
                if(bootOption==='disk') {
                    return '硬盘启动'
                }else if(bootOption==='cdrom') {
                    return '光驱启动'
                }else if(bootOption==='pxe') {
                    return '网络启动'
                }
            },
            // 格式化安全虚拟机类型
            safeTypeFormat(safeType) {
                if(this.svm===false) {
                    return '未开启'
                }else {
                    if(safeType==='secureVmType') {
                        return '防病毒'
                    }else if(safeType==='dpiVmType') {
                        return 'DPI'
                    }
                }
            },
            securiteTypeFormat() {
                if(this.svm===false) {
                    return '未开启'
                }else {
                    return this.secureVmTypeTo
                }
            },
            // 格式化虚机状态
            statusFormat(row) {
                if (row.status === 'stopped') {
                    return '已停止';
                }else if (row.status === 'running') {
                    return '运行中';
                }else if (row.status === 'unknown') {
                    return '不明确';
                }else if (row.status === 'hibernated') {
                    return '已休眠';
                }else if (row.status === 'creating') {
                    return '创建中或模板正在部署虚拟机或正在导入模板';
                }else if (row.status === 'shutting-down') {
                    return '删除中';
                }else if (row.status === 'migrating') {
                    return '迁移中';
                }else if (row.status === 'fault-resuming') {
                    return '故障恢复中';
                }else if (row.status === 'starting') {
                    return '启动中';
                }else if (row.status === 'stopping') {
                    return '停止中';
                }else if (row.status === 'hibernating') {
                    return '休眠中';
                }else if (row.status === 'pause') {
                    return '已暂停';
                }else if (row.status === 'recycling') {
                    return '回收中';
                }
            },
            // 格式化虚机类型
            typeFormat(row) {
                if (row.vmType === 0) {
                    return '普通虚拟机';
                }else if(row.vmType === 1){
                    return '容灾虚拟机';
                }else if(row.vmType === 2){
                    return '占位虚拟机';
                }
            },
            // 格式化数据存储精简配置
            storageisThinFormat(row) {
                if(row.isThin===true) {
                    return '支持'
                }else {
                    return '不支持'
                }
            },
            // 格式化数据存储锁类型
            storageLockTypeFormat(row) {
                if(row.dsLockType===0) {
                    return '-'
                }else if(row.dsLockType===1) {
                    return '分布式锁'
                }else if(row.dsLockType===2) {
                    return '硬件辅助锁'
                }
            },
            // 端口类型格式化
            portTypeFormat(row) {
                if(row.portType===0) {
                    return 'Access'
                }else if(row.portType===1) {
                    return 'Trunk'
                }
            },
            storageTypeFormat(row) {
                if(row.storageType==='LOCALPOME') {
                    return '虚拟化的本地存储';
                }else if(row.storageType==='local') {
                    return '本地存储';
                }else if(row.storageType==='san') {
                    return '共享存储(大lun)';
                }else if(row.storageType==='advanceSan') {
                    return '共享存储(小lun)';
                }else if(row.storageType==='DSWARE') {
                    return '华为分布式存储系统';
                }else if(row.storageType==='NAS') {
                    return 'NAS存储';
                }else if(row.storageType==='LUNPOME') {
                    return '虚拟化的共享存储(大LUN)';
                }else if(row.storageType==='LUN') {
                    return '裸设备映射的共享存储';
                }else if(row.storageType==='iotailor') {
                    return '本地内存盘';
                }
            },
            // 获取华为云环境数据
            getHuaweiyunData() {
                this.$http.get(`automation/api/huawei/`, {
                    headers: {
                        'token': this.token,
                    }
                }).then((res) => {
                    if(sessionStorage.getItem('huaweiyun_env')) {
                        this.huaweiyun_env = JSON.parse(sessionStorage.getItem('huaweiyun_env')).hw_ip;
                    }else {
                        sessionStorage.setItem('huaweiyun_env', JSON.stringify(res.data[0]));
                        this.huaweiyun_env = res.data[0].hw_ip;
                    }
                    this.huaweiyun_options = res.data;
                    this.getData();
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 获取 easy-mock 的模拟数据
            getData() {
                let keyword = this.keywords;
                let url = this.url;
                if (keyword) {
                    url=`automation/api/huawei/vms/?Template=false&name=${keyword}`
                }else {
                    url=`automation/api/huawei/vms/?Template=false`
                }
                this.$http.get(`${url}`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    res.data.vms.map( item =>{
                        item['id']=item['uri'].split("/")[5];
                        item['ip']=item['vmConfig'].nics[0].ip;
                    });
                    this.tableData = res.data.vms;
                    this.pageTotal = res.data.total;
                    this.loading = false;
                }).catch(  (error) =>{
                    console.log(error);
                    this.$message.error('查询失败！');
                    this.loading = false;
                });
            },
            // 触发选择环境操作
            handleSelectHuaweiEnv(val) {
                this.tableData = [];
                this.handleSetHuaweiEnvInfo(val);
                sessionStorage.setItem('huaweiyun_env', JSON.stringify(this.huaweiyun_env_info));
                this.getData();
            },
            // 遍历华为云环境信息
            handleSetHuaweiEnvInfo(val) {
                for(var j = 0, len=this.huaweiyun_options.length; j < len; j++) {
                    if(this.huaweiyun_options[j].hw_ip===val) {
                        return this.huaweiyun_env_info = this.huaweiyun_options[j];
                    }
                }
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            // 触发删除按钮
            handleDeleteVms(index, row) {
                this.id = row.id;
                this.vms_name = row.name;
                this.deleteVisible = true;
            },
            // 删除操作
            deleteVms() {
                this.$http.delete(`automation/api/huawei/delete_vms/?id=${this.id}&isFormat=0&holdTime=0`,
                    {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                    if(res.status === 200 || res.status === 204) {
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
                this.currentSelectDataStore = val.name;
                this.currentSelectDataStoreUrn = val.urn;
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
            // 创建步骤
            handleStepOPtions(tab) {
                this.locationTo='';
                // this.form.location='';
                // this.form.vmsTemplate='';
                this.form = {
                    name: "New Virtual Machine",
                    description: "",
                    parentObjUrn: "",
                    vmsTemplate: "",
                    location: "",
                    osOptions: {
                        osType: "Windows",
                        osVersion: "",
                    },
                    vmConfig: {
                        cpu: {
                            weight: 1000,
                            reservation: 0,
                            quantity: 2,
                            limit: 0,
                            coresPerSocket: 1
                        },
                        memory: {
                            quantityMB: 4,
                            reservation: 0,
                            weight: 40960,
                            limit: 0
                        },
                        disks: [{
                            datastoreUrn: "",
                            name: "autoDS_CNA001",
                            quantityGB: 40,
                            sequenceNum: 1,
                            isThin: false,
                            pciType: "VIRTIO",
                            volType: 1,
                        }],
                        nics: [{
                            sequenceNum: 0,
                            portGroupUrn: "",
                            virtIo: 1,
                            nicConfig: {
                                vringbuf: 256,
                                queues: 1
                            },
                            enableSecurityGroup: false,
                        }],
                        properties: {
                            clockMode: false,
                            bootFirmware: "BIOS",
                            evsAffinity: false,
                            bootFirmwareTime: 0,
                            bootOption: "disk",
                            vmVncKeymapSetting: 7,
                            isAutoAdjustNuma: false,
                            safeType: "secureVmType"
                        }
                    },
                    isBindingHost: false,
                    autoBoot: true,
                    vmSize: 1,
                    namePostfixIndex: 0,
                };
                this.show_cpu = false;
                this.cpu_arrow_icon = 'el-icon-caret-right';
                this.show_mem = false;
                this.mem_arrow_icon = 'el-icon-caret-right';
                this.show_network = false;
                this.network_arrow_icon = 'el-icon-caret-right';
                this.show_disk = false;
                this.disk_arrow_icon = 'el-icon-caret-right';
                this.cpu_share = '中';
                this.mem_share = '中';
                this.selectOsType();
                if(tab.name==="0") {
                    this.step_options = [
                        {
                            value: '选项1',
                            label: '选择创建类型'
                        }, {
                            value: '选项2',
                            label: '基本配置'
                        }, {
                            value: '选项3',
                            label: '选择数据存储'
                        }, {
                            value: '选项4',
                            label: '虚拟机配置'
                        }, {
                            value: '选项5',
                            label: '确认信息'
                        }
                    ]
                    this.showOption=true;
                }else if(tab.name==="1") {
                    this.step_options = [
                        {
                            value: '选项1',
                            label: '选择创建类型'
                        }, {
                            value: '选项2',
                            label: '基本配置'
                        }, {
                            value: '选项3',
                            label: '虚拟机配置'
                        }, {
                            value: '选项4',
                            label: '确认信息'
                        }
                    ]
                }
            },
            // 查询站点信息
            selectVmPosition() {
                this.$http.get(`automation/api/huawei/sites/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.position_data = res.data.sites;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 选择虚拟机位置操作
            handleSelectPosition() {
                this.selectVmPosition();
                this.positionVisible = true;
            },
            // 添加位置操作
            handlePositionClick(data) {
                this.select_vm_position = data.urn;
            },
            // 添加位置操作
            addPosition() {
                this.form.parentObjUrn = this.select_vm_position;
                this.positionVisible = false;
            },
            // 取消添加操作
            cancelPosition() {
                this.positionVisible = false;
            },
            // 选择虚拟机计算资源操作
            handleSelectCluster() {
                this.clusterVisible = true;
            },
            // 加载节点信息
            loadNode(node, resolve) {
                if (node.level === 0) {
                    this.$http.get(`automation/api/huawei/sites/`, {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                        this.position_data = res.data.sites;
                        return resolve(this.position_data);
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else if(node.level === 1) {
                    this.$http.get(`automation/api/huawei/clusters/`, {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                        this.cluster_data = res.data.clusters;
                        return resolve(this.cluster_data);
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else if(node.level === 2) {
                    this.$http.get(`automation/api/huawei/hosts?scope=${node.data.urn}`, {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                        this.host_data = res.data.hosts;
                        return resolve(this.host_data);
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }

                if (node.level > 2) return resolve([]);
                },
            // 添加集群操作
            handleClusterClick(data, Node) {
                if(Node.level===2 && Node.childNodes.length===0) {
                    this.select_level=4;
                    this.$alert('该节点下没有可用主机，请重新选择', '提示', {
                        confirmButtonText: '确定',
                    }).catch(e=>e);
                }else if(Node.parent.parent==null) {
                    this.select_level=4;
                    this.$alert('该节点不能作为计算资源被选择，请重新选择', '提示', {
                        confirmButtonText: '确定',
                    }).catch(e=>e);
                }else {
                    this.select_vm_cluster = data.urn;
                    this.select_vm_cluster_to = data.label;
                    this.select_level = Node.level;
                }
            },
            // 添加集群操作
            addCluster() {
                this.locationTo = this.select_vm_cluster_to;
                this.form.location = this.select_vm_cluster;
                if(this.select_level===3) {
                    this.checked_disabled = false;
                    this.clusterVisible = false;
                }else if(this.select_level===4) {
                    this.$alert('请选择集群和主机。', '提示', {
                        confirmButtonText: '确定',
                    }).catch(e=>e);
                }else {
                    this.checked_disabled = true;
                    this.clusterVisible = false;
                }
            },
            // 取消添加操作
            cancelCluster() {
                this.clusterVisible = false;
            },
            // 查询数据存储操作
            getDatastore() {
                this.$http.get(`automation/api/huawei/datastores/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.storeTableData = res.data.datastores;
                }).catch(  (error) => {
                    console.log(error);
                    this.$message.error('查询失败！');
                });
            },
            // 选择磁盘数据存储操作
            handleSelectDataStore() {
                this.dataStoreVisible = true;
            },
            // 选择数据存储操作
            handleDataStoreChange(val) {
                this.currentSelectDataStore = val.name;
                this.currentSelectDataStoreUrn = val.urn;
            },
            // 取消添加
            cancelDataStore() {
                this.dataStoreVisible = false;
            },
            // 添加数据存储操作
            addDataStore() {
                this.form.vmConfig.disks[0].name = this.currentSelectDataStore;
                this.form.vmConfig.disks[0].datastoreUrn = this.currentSelectDataStoreUrn;
                this.dataStoreVisible = false;
            },
            // 查询交换机操作
            getDVSwitchData() {
                this.$http.get(`automation/api/huawei/dvswitch/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    let svswitch_data=res.data.dvSwitchs;
                    let temp_obj=[];
                    svswitch_data.map( item =>{
                        temp_obj.push({'label': item.name, 'value': item.portGroupNum});
                    });
                    this.dv_switch_options = temp_obj;
                    this.form.dv_switch = svswitch_data[0].name;
                    this.getPortGroupData(svswitch_data[0].portGroupNum);
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 查询端口组操作
            getPortGroupData(port_group_num) {
                this.$http.get(`automation/api/huawei/portgroups?portGroupNum=${port_group_num}`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.portGroupTableData = res.data.portGroups;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 选择网卡交换机操作
            handleNetworkSwitch() {
                this.getDVSwitchData();
                this.networkSwitchVisible = true;
            },
            // 查询端口组num操作
            handleSetPortGroupNum(val) {
                this.getPortGroupData(val);
            },
            // 选择端口组操作
            handlePortGroupChange(val) {
                this.currentSelectPortGroup = val.urn;
            },
            // 取消添加端口组
            cancelPortGroup() {
                this.networkSwitchVisible = false;
            },
            // 添加端口组
            addPortGroup() {
                this.form.vmConfig.nics[0].portGroupUrn = this.currentSelectPortGroup;
                this.networkSwitchVisible = false;
            },
            // 查询安全组信息
            getSecurityGroupData() {
                this.$http.get(`automation/api/huawei/securitygroups`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.securityGroupTableData = res.data.securityGroups;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 选择网卡安全组操作
            handleSelectSecurityGroup() {
                this.getSecurityGroupData();
                this.securityGroupVisible = true;
            },
            // 选择安全组操作
            handleSecurityGroupChange(val) {
                this.currentSelectSecurityGroup = val.sgId;
            },
            // 取消添加安全组
            cancelSecurityGroup() {
                this.securityGroupVisible = false;
            },
            // 添加安全组
            addSecurityGroup() {
                this.form.vmConfig.nics[0].securityGroupId = this.currentSelectSecurityGroup;
                this.securityGroupVisible = false;
            },
            // 选择显卡操作
            handleSelectGpuSize() {
                if(this.form.gpu==='Cirrus') {
                    this.gpu_size_options = [4]
                }else if(this.form.gpu==='VGA') {
                    this.gpu_size_options = [4, 8, 16, 32, 64, 128, 256]
                }
            },
            // 查询虚拟机模板信息
            selectVmsTemplate() {
                this.$http.get(`automation/api/huawei/vms/?Template=true`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.templateTableData = res.data.vms;
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 选择虚拟机模板操作
            handleSelectTemplate() {
                this.selectVmsTemplate();
                this.templateVisible = true;
            },
            // 选择模板操作
            handleTemplateChange(val) {
                this.currentSelectTemplate = val;
            },
            // 添加模板操作
            addTemplate() {
                if(this.currentSelectTemplate) {
                    this.form.vmsTemplate = this.currentSelectTemplate.name;
                    this.locationTo = this.currentSelectTemplate.locationName;
                    this.form.name = this.currentSelectTemplate.name;
                    this.form.location = this.currentSelectTemplate.location;
                    this.form.vmConfig.cpu = this.currentSelectTemplate.vmConfig.cpu;
                    this.form.vmConfig.memory = this.currentSelectTemplate.vmConfig.memory;
                    this.form.vmConfig.disks[0].datastoreUrn = this.currentSelectTemplate.vmConfig.disks[0].datastoreUrn;
                    this.form.vmConfig.disks[0].name = this.currentSelectTemplate.vmConfig.disks[0].name;
                    this.form.vmConfig.disks[0].quantityGB = this.currentSelectTemplate.vmConfig.disks[0].quantityGB;
                    this.form.vmConfig.disks[0].sequenceNum = this.currentSelectTemplate.vmConfig.disks[0].sequenceNum;
                    this.form.vmConfig.disks[0].indepDisk = this.currentSelectTemplate.vmConfig.disks[0].indepDisk;
                    this.form.vmConfig.disks[0].persistentDisk = this.currentSelectTemplate.vmConfig.disks[0].persistentDisk;
                    this.form.vmConfig.disks[0].systemVolume = this.currentSelectTemplate.vmConfig.disks[0].systemVolume;
                    this.form.vmConfig.disks[0].isThin = this.currentSelectTemplate.vmConfig.disks[0].isThin;
                    this.form.vmConfig.disks[0].pciType = this.currentSelectTemplate.vmConfig.disks[0].pciType;
                    this.form.vmConfig.disks[0].volType = this.currentSelectTemplate.vmConfig.disks[0].volType;
                    this.form.vmConfig.nics[0].sequenceNum = this.currentSelectTemplate.vmConfig.nics[0].sequenceNum;
                    this.form.vmConfig.nics[0].portGroupUrn = this.currentSelectTemplate.vmConfig.nics[0].portGroupUrn;
                    this.form.vmConfig.nics[0].virtIo = this.currentSelectTemplate.vmConfig.nics[0].virtIo;
                    this.form.vmConfig.nics[0].nicConfig = this.currentSelectTemplate.vmConfig.nics[0].nicConfig;
                    this.form.vmConfig.nics[0].enableSecurityGroup = this.currentSelectTemplate.vmConfig.nics[0].enableSecurityGroup;
                    this.form.vmConfig.properties.clockMode = this.currentSelectTemplate.vmConfig.properties.clockMode;
                    this.form.vmConfig.properties.bootFirmware = this.currentSelectTemplate.vmConfig.properties.bootFirmware;
                    this.form.vmConfig.properties.bootFirmwareTime = this.currentSelectTemplate.vmConfig.properties.bootFirmwareTime;
                    this.form.vmConfig.properties.bootOption = this.currentSelectTemplate.vmConfig.properties.bootOption;
                    this.form.vmConfig.properties.evsAffinity = this.currentSelectTemplate.vmConfig.properties.evsAffinity;
                    this.form.vmConfig.properties.vmVncKeymapSetting = this.currentSelectTemplate.vmConfig.properties.vmVncKeymapSetting;
                    this.form.vmConfig.properties.isAutoUpgrade = this.currentSelectTemplate.vmConfig.properties.isAutoUpgrade;
                    this.form.vmConfig.properties.attachType = this.currentSelectTemplate.vmConfig.properties.attachType;
                    this.form.vmConfig.properties.isEnableMemVol = this.currentSelectTemplate.vmConfig.properties.isEnableMemVol;
                    this.form.vmConfig.properties.isEnableFt = this.currentSelectTemplate.vmConfig.properties.isEnableFt;
                    this.form.vmConfig.properties.isAutoAdjustNuma = this.currentSelectTemplate.vmConfig.properties.isAutoAdjustNuma;
                    this.form.vmConfig.properties.secureVmType = this.currentSelectTemplate.vmConfig.properties.secureVmType;
                    this.form.vmConfig.properties.dpiVmType = this.currentSelectTemplate.vmConfig.properties.dpiVmType;
                    this.form.osOptions = this.currentSelectTemplate.osOptions;
                    this.form.isBindingHost = this.currentSelectTemplate.isBindingHost;
                    this.form.description = this.currentSelectTemplate.description;
                    this.form.autoBoot = false;
                    this.template_id = this.currentSelectTemplate.uri.split("/")[5];
                    this.selectOsType();
                    this.templateVisible = false;
                }else {
                    this.$message.warning('请选择一个模板！');
                }
            },
            // 取消添加操作
            cancelTemplate() {
                this.templateVisible = false;
            },
            // 上一步操作
            prevStep() {
                this.active--;
                if(this.active===0) {
                    this.prev_disabled=true;
                }else {
                    this.prev_disabled=false;
                }
                this.next_step='下一步';
            },
            // 下一步操作
            nextStep() {
                if(this.next_step==='下一步') {
                this.active++;
                this.prev_disabled=false;
                if(this.activeName==='0' && this.active===1) {
                    this.$http.get(`automation/api/huawei/sites/`, {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                        this.position_data = res.data.sites;
                        this.form.parentObjUrn = this.position_data[0].urn;
                        this.parentObjUrnTo = this.position_data[0].label;
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else if(this.activeName==='0' && this.active===2) {
                    this.$refs.form.validate((valid) => {
                        if(valid) {
                            this.$http.get(`automation/api/huawei/datastores/`, {
                                headers:{
                                    'token': this.token,
                                    'env': sessionStorage.getItem('huaweiyun_env')
                                }
                            }).then((res)=>{
                                this.storeTableData = res.data.datastores;
                                this.$refs.singleTable.setCurrentRow(this.storeTableData[0]);
                            }).catch(  (error) => {
                                this.$message.error(JSON.stringify(error.response.data));
                            });
                        } else {
                            this.active--;
                            this.$message.warning('请选择必填项');
                        }
                    });
                }else if(this.activeName==='0' && this.active===3) {
                    // 磁盘存储空间默认值
                    this.form.vmConfig.disks[0].name = this.currentSelectDataStore;
                    this.form.vmConfig.disks[0].datastoreUrn = this.currentSelectDataStoreUrn;
                    // 交换机端口默认值
                    this.$http.get(`automation/api/huawei/dvswitch/`, {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                        let svswitch_data=res.data.dvSwitchs;
                        let temp_obj=[];
                        svswitch_data.map( item =>{
                            temp_obj.push({'label': item.name, 'value': item.portGroupNum});
                        });
                        this.dv_switch_options = temp_obj;
                        this.form.dv_switch = svswitch_data[0].name;
                        this.$http.get(`automation/api/huawei/portgroups?portGroupNum=${svswitch_data[0].portGroupNum}/`, {
                            headers:{
                                'token': this.token,
                                'env': sessionStorage.getItem('huaweiyun_env')
                            }
                        }).then((res)=>{
                            this.portGroupTableData = res.data.portGroups;
                            this.form.vmConfig.nics[0].portGroupUrn = this.portGroupTableData[0].urn;
                            this.portGroupUrnTo = this.portGroupTableData[0].name;
                        }).catch(  (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }else if(this.activeName==='0' && this.active===4) {
                    console.log(this.form.vmConfig.properties.clockMode);
                    this.next_step='确认';
                }else if(this.activeName==='1' && this.active===1) {
                        this.$http.get(`automation/api/huawei/sites/`, {
                            headers:{
                                'token': this.token,
                                'env': sessionStorage.getItem('huaweiyun_env')
                            }
                        }).then((res)=>{
                            this.position_data = res.data.sites;
                            this.form.parentObjUrn = this.position_data[0].urn;
                            this.parentObjUrnTo = this.position_data[0].label;
                        }).catch(  (error) => {
                            this.$message.error(JSON.stringify(error.response.data));
                        });
                }else if(this.activeName==='1' && this.active===2) {
                    this.$refs.form.validate((valid) => {
                        if(valid) {
                            this.form.vmConfig.memory.quantityMB = this.currentSelectTemplate.vmConfig.memory.quantityMB / 1024;
                            this.form.vmConfig.disks[0].name = this.currentSelectTemplate.vmConfig.disks[0].datastoreName;
                            this.portGroupUrnTo = this.currentSelectTemplate.vmConfig.nics[0].portGroupName;
                        } else {
                            this.active--;
                            this.$message.warning('请选择必填项');
                        }
                    });
                }else if(this.activeName==='1' && this.active===3) {
                    this.next_step='确认';
                }}else if(this.activeName==='0' && this.next_step==='确认') {
                    // 时钟策略默认值
                    if(this.form.vmConfig.properties.clockMode===false) {
                        this.form.vmConfig.properties.clockMode = "freeClock";
                    }else {
                        this.form.vmConfig.properties.clockMode = "synchClock";
                    }
                    if(this.svm===false) {
                        delete this.form.vmConfig.properties.safeType;
                        delete this.form.vmConfig.properties.secureVmType;
                        delete this.form.vmConfig.properties.dpiVmType;
                    }
                    this.form.vmConfig.memory.quantityMB = this.form.vmConfig.memory.quantityMB * 1024;
                    this.$http.post(`automation/api/huawei/create_vms/`,
                        this.form,
                        {
                            headers:{
                                'token': this.token,
                                'env': sessionStorage.getItem('huaweiyun_env')
                            }
                        }).then((res)=>{
                        if(res.status === 200 || res.status === 201) {
                            this.$message.success('创建成功！');
                            this.editVisible = false;
                            this.getData();
                        }else{
                            this.$message.error('创建失败！');
                        }
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data.errorDes));
                    });
                }else if(this.activeName==='1' && this.next_step==='确认') {
                    delete this.form.vmsTemplate;
                    if(this.svm===false) {
                        delete this.form.vmConfig.properties.safeType;
                        delete this.form.vmConfig.properties.secureVmType;
                        delete this.form.vmConfig.properties.dpiVmType;
                    }
                    if(this.form.vmSize===1) {
                        delete this.form.vmSize;
                        delete this.form.namePostfixIndex;
                    }
                    this.form.vmConfig.memory.quantityMB = this.form.vmConfig.memory.quantityMB * 1024;
                    console.log('form', this.form);
                    this.$http.post(`automation/api/huawei/clone_vms/?id=${this.template_id}`,
                        this.form,
                        {
                            headers:{
                                'token': this.token,
                                'env': sessionStorage.getItem('huaweiyun_env')
                            }
                        }).then((res)=>{
                        if(res.status === 200 || res.status === 201) {
                            this.$message.success('创建成功！');
                            this.editVisible = false;
                            this.getData();
                        }else{
                            this.$message.error('创建失败！');
                        }
                    }).catch(  (error) => {
                        this.$message.error(JSON.stringify(error.response.data.errorDes));
                    });
                }
            },
            // 虚拟机配置点击操作
            handleVMClick(tab, event) {
                console.log(tab, event);
            },
            // 配置CPU数量操作
            handleCPUChange() {
                if(this.cpu_share==='低') {
                    this.form.vmConfig.cpu.weight = this.form.vmConfig.cpu.quantity*250;
                }else if(this.cpu_share==='中') {
                    this.form.vmConfig.cpu.weight = this.form.vmConfig.cpu.quantity*500;
                }else if(this.cpu_share==='高') {
                    this.form.vmConfig.cpu.weight = this.form.vmConfig.cpu.quantity*1000;
                }
            },
            // 配置mem大小操作
            handleMemChange() {
                if(this.mem_share==='低') {
                    this.form.vmConfig.memory.weight = this.form.vmConfig.memory.quantityMB*1024*5;
                }else if(this.mem_share==='中') {
                    this.form.vmConfig.memory.weight = this.form.vmConfig.memory.quantityMB*1024*10;
                }else if(this.mem_share==='高') {
                    this.form.vmConfig.memory.weight = this.form.vmConfig.memory.quantityMB*1024*20;
                }
            },
            showSystemInfo() {
                this.show_system = !this.show_system
                if(this.arrow==='>>') {
                    this.arrow='<<';
                } else {
                    this.arrow='>>';
                }
            },
            // 显示CPU详情信息
            showCPUInfo() {
                this.show_cpu = !this.show_cpu
                if(this.cpu_arrow_icon==='el-icon-caret-right') {
                    this.cpu_arrow_icon='el-icon-caret-bottom';
                } else {
                    this.cpu_arrow_icon='el-icon-caret-right';
                }
            },
            // 显示内存详情信息
            showMemInfo() {
                this.show_mem = !this.show_mem
                if(this.mem_arrow_icon==='el-icon-caret-right') {
                    this.mem_arrow_icon='el-icon-caret-bottom';
                } else {
                    this.mem_arrow_icon='el-icon-caret-right';
                }
            },
            // 显示网卡详情信息
            showNetworkInfo() {
                this.show_network = !this.show_network
                if(this.network_arrow_icon==='el-icon-caret-right') {
                    this.network_arrow_icon='el-icon-caret-bottom';
                } else {
                    this.network_arrow_icon='el-icon-caret-right';
                }
            },
            // 显示磁盘详情信息
            showDiskInfo() {
                this.show_disk = !this.show_disk
                if(this.disk_arrow_icon==='el-icon-caret-right') {
                    this.disk_arrow_icon='el-icon-caret-bottom';
                } else {
                    this.disk_arrow_icon='el-icon-caret-right';
                }
            },
            // 绑定策略状态修改
            handleBandCategory() {
                this.cpu_disabled = !this.cpu_disabled
            },
            // CPU份额操作
            handleCpuShare() {
                if(this.cpu_share==='自定义') {
                    this.cpu_share_disabled=false;
                }else if(this.cpu_share==='低') {
                    this.form.vmConfig.cpu.weight=this.form.vmConfig.cpu.quantity*250;
                    this.cpu_share_disabled=true;
                }else if(this.cpu_share==='中') {
                    this.form.vmConfig.cpu.weight=this.form.vmConfig.cpu.quantity*500;
                    this.cpu_share_disabled=true;
                }else if(this.cpu_share==='高') {
                    this.form.vmConfig.cpu.weight=this.form.vmConfig.cpu.quantity*1000;
                    this.cpu_share_disabled=true;
                }
            },
            // 内存份额操作
            handleMemShare() {
                if(this.mem_share==='自定义') {
                    this.mem_share_disabled=false;
                }else if(this.mem_share==='低') {
                    this.form.vmConfig.memory.weight=this.form.vmConfig.memory.quantityMB*1024*5;
                    this.mem_share_disabled=true;
                }else if(this.mem_share==='中') {
                    this.form.vmConfig.memory.weight=this.form.vmConfig.memory.quantityMB*1024*10;
                    this.mem_share_disabled=true;
                }else if(this.mem_share==='高') {
                    this.form.vmConfig.memory.weight=this.form.vmConfig.memory.quantityMB*1024*20;
                    this.mem_share_disabled=true;
                }
            },
            // 虚拟机数量选择操作
            handleAddVmSize() {
                if(this.form.vmSize > 1) {
                    this.postfix_index_disabled = false;
                }else {
                    this.postfix_index_disabled = true;
                }
            },
            // 大页配置操作
            handleLargePageConfig() {
                if(this.form.large_page_config!=='未开启') {
                    this.mem_reserve_disabled=true;
                    this.mem_limit_disabled=true;
                }else {
                    this.mem_reserve_disabled=false;
                    this.mem_limit_disabled=false;
                }
            },
            // 选择磁盘类型操作
            handleSelectVolType() {
                if(this.form.vmConfig.disks[0].volType===3) {
                    this.form.vmConfig.disks[0].isThin = true;
                }
            },
            // 打开安全虚拟机操作
            handleSwitchSvm() {
                if(this.svm===true) {
                    this.form.vmConfig.properties.safeType="secureVmType";
                    this.form.vmConfig.properties.secureVmType="GVM";
                }
            },
            // 选择安全虚拟机操作
            handleSwitchSecureVm() {
                if(this.form.vmConfig.properties.safeType==="dpiVmType") {
                    this.form.vmConfig.properties.dpiVmType = this.secureVmTypeTo;
                    delete this.form.vmConfig.properties.secureVmType;
                }else if(this.form.vmConfig.properties.safeType==="secureVmType") {
                    this.form.vmConfig.properties.secureVmType = this.secureVmTypeTo;
                    delete this.form.vmConfig.properties.dpiVmType;
                }
            },
            // 选择安全组操作
            handleSwitchSecurityGroup() {
              if(this.form.vmConfig.nics[0].enableSecurityGroup) {
                  this.form.vmConfig.nics[0].securityGroupId = "";
              }else {
                  delete this.form.vmConfig.nics[0].securityGroupId;
              }
            },
            // 恢复默认值操作
            handleRestoreDefault() {
                this.form.vmConfig.properties.clockMode = "freeClock";
                this.form.vmConfig.properties.bootFirmware = "BIOS";
                this.form.vmConfig.properties.evsAffinity=false;
                this.form.vmConfig.properties.bootFirmwareTime=0;
                this.form.vmConfig.properties.bootOption="disk";
                this.form.vmConfig.properties.vmVncKeymapSetting=7;
                this.form.vmConfig.properties.isAutoAdjustNuma=false;
                this.form.vmConfig.properties.safeType= "secureVmType";
                this.form.vmConfig.properties.secureVmType="GVM";
                this.svm=false;
            },
            // 选择延迟时间操作
            handleSelectBootFirmware(val) {
                if(val==='UEFI') {
                    this.firmware_time_disabled = true;
                }else {
                    this.firmware_time_disabled = false;
                }
            },
            // 创建虚拟机操作
            handleCreate() {
                this.active = 0;
                this.activeName = "0";
                this.next_step = "下一步";
                this.prev_disabled = true;
                this.locationTo = '';
                this.editVisible = true;
                this.form = {
                    name: "New Virtual Machine",
                    description: "",
                    parentObjUrn: "",
                    vmsTemplate: "",
                    location: "",
                    osOptions: {
                        osType: "Windows",
                        osVersion: "",
                    },
                    vmConfig: {
                        cpu: {
                            weight: 1000,
                            reservation: 0,
                            quantity: 2,
                            limit: 0,
                            coresPerSocket: 1
                        },
                        memory: {
                            quantityMB: 4,
                            reservation: 0,
                            weight: 40960,
                            limit: 0
                        },
                        disks: [{
                            datastoreUrn: "",
                            name: "autoDS_CNA001",
                            quantityGB: 40,
                            sequenceNum: 1,
                            isThin: false,
                            pciType: "VIRTIO",
                            volType: 1,
                        }],
                        nics: [{
                            sequenceNum: 0,
                            portGroupUrn: "",
                            virtIo: 1,
                            nicConfig: {
                                vringbuf: 256,
                                queues: 1
                            },
                            enableSecurityGroup: false,
                        }],
                        properties: {
                            clockMode: false,
                            bootFirmware: "BIOS",
                            evsAffinity: false,
                            bootFirmwareTime: 0,
                            bootOption: "disk",
                            vmVncKeymapSetting: 7,
                            isAutoAdjustNuma: false,
                            safeType: "secureVmType"
                        }
                    },
                    isBindingHost: false,
                    autoBoot: true,
                    vmSize: 1,
                    namePostfixIndex: 0,
                };
                this.show_cpu = false;
                this.cpu_arrow_icon = 'el-icon-caret-right';
                this.show_mem = false;
                this.mem_arrow_icon = 'el-icon-caret-right';
                this.show_network = false;
                this.network_arrow_icon = 'el-icon-caret-right';
                this.show_disk = false;
                this.disk_arrow_icon = 'el-icon-caret-right';
                this.cpu_share = '中';
                this.mem_share = '中';
                this.selectOsType();
                this.getDatastore();
                this.cpu_band_category_options = ['prefer'];
                this.cpu_share_options = ['低', '中', '高', '自定义'];
                this.large_page_config_options = ['未开启', '2M', '1G'];
                this.config_mode_options = [{name: '普通延迟置零', value: 1}, {name: '普通', value: 0}, {name: '精简', value: 3}];
                this.disk_mode_options = ['从属', '独立-持久', '独立-非持久'];
                this.bus_type_options = ['VIRTIO', 'IDE', 'SCSI'];
                this.network_type_options = [{name: 'virtio', value: 1}];
                this.IO_ring_num_options = [256, 512, 1024, 2048, 4096];
                this.gpu_options = ['Cirrus', 'VGA'];
                this.gpu_size_options = [4];
                this.boot_mode_options = [{name: '网络启动', value: 'pxe'}, {name: '光驱启动', value: 'cdrom'}, {name: '硬盘启动', value: 'disk'}];
                this.getFloppydriver();
                this.getVNCKeyboard();
                this.security_type_options = [{name: "防病毒", value: "secureVmType"}, {name: "DPI", value: "dpiVmType"}];
                this.vm_security_type_options = ['GVM', 'SVM'];
            },
            // 触发选择系统类型
            selectOsType() {
                this.$http.get(`automation/api/huawei/vms/osversions/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    // console.log('windows', res.data.windows[1]);
                    if(this.form.osOptions.osType==='Windows') {
                        this.form.osOptions.osVersion = 203
                        this.os_version_options = res.data.windows;
                    }else if(this.form.osOptions.osType==='Linux') {
                        this.form.osOptions.osVersion = 169;
                        this.os_version_options = res.data.linux;
                    }else {
                        this.form.osOptions.osVersion = 401;
                        this.os_version_options = res.data.other;
                    }
                }).catch(  (error) => {
                    console.log(error);
                    this.$message.error('查询失败！');
                });
            },
            // 查询软驱信息
            getFloppydriver() {
                this.$http.get(`automation/api/huawei/queryVfdFiles/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.floppy_drive_options = res.data.VfdFiles;
                }).catch(  (error) => {
                    console.log(error);
                    this.$message.error('查询失败！');
                });
            },
            // 查询键盘配置信息
            getVNCKeyboard() {
                this.$http.get(`automation/api/huawei/vncKeymapSettings/`, {
                    headers:{
                        'token': this.token,
                        'env': sessionStorage.getItem('huaweiyun_env')
                    }
                }).then((res)=>{
                    this.vnc_keyboard_options = res.data.vmVncKeymapSettings;
                }).catch(  (error) => {
                    console.log(error);
                    this.$message.error('查询失败！');
                });
            },
            // 自动启动操作
            handleAutoBoot() {
                this.form.autoBoot = !this.form.autoBoot;
            },
            // 触发删除按钮
            handleStopVms(index, row) {
                this.id = row.id;
                this.vms_name = row.name;
                this.stopVisible = true;
            },
            // 停止虚拟机操作
            stopVms() {
                this.$http.post(`automation/api/huawei/stop_vms/?id=${this.id}`,
                    {mode: "safe"},
                    {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                    if(res.status === 200 || res.status === 201) {
                        this.$message.success('虚拟机停止成功！');
                        this.stopVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('虚拟机停止失败！');
                        this.stopVisible = false;
                    }
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data.errorDes));
                    this.stopVisible = false;
                });
            },
            // 触发删除按钮
            handleStartVms(index, row) {
                this.id = row.id;
                this.vms_name = row.name;
                this.startVisible = true;
            },
            // 开启虚拟机操作
            startVms() {
                this.$http.post(`automation/api/huawei/start_vms/?id=${this.id}`,
                    null,
                    {
                        headers:{
                            'token': this.token,
                            'env': sessionStorage.getItem('huaweiyun_env')
                        }
                    }).then((res)=>{
                    if(res.status === 200 || res.status === 201) {
                        this.$message.success('虚拟机开启成功！');
                        this.startVisible = false;
                        this.getData();
                    }else{
                        this.$message.error('虚拟机开启失败！');
                        this.startVisible = false;
                    }
                }).catch(  (error) => {
                    this.$message.error(JSON.stringify(error.response.data.errorDes));
                    this.startVisible = false;
                });
            },
            // 分页导航
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
        },
        // components: {
        //     'editor': Editor,
        // }
    };
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    @import "../../../../public/tinymce/skins/ui/oxide/skin.css";
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
    .border-left {
        height: 350px;
        padding: 20px;
        border: 1px solid #c5c3c3
    }
    .border-right {
        height: 310px;
        padding: 20px;
        margin: 20px;
        border: 1px solid #c5c3c3
    }
    .border-right-next {
        padding-left: 20px;
    }
    .create-input {
        width: 250px;
    }
    .select-dialog-div {
        height: 230px;
        overflow: auto;
    }
    .vm-dialog-div {
        height: 420px;
        overflow: auto;
    }
    .el-divider--horizontal{
        margin: 8px 0;
        background: 0 0;
        border-top: 1px dashed #c2bfbf;
    }
    .horizontal{
        margin: 8px 0;
        background: 0 0;
        border-top: 1px solid #c2bfbf;
    }
    .mt10{
        margin-top: 10px;
    }
    /*/deep/ .vm-dialog-div{
        scrollbar-width:none; !* Firefox *!
        -ms-overflow-style: none; !* IE 10+ *!
    }
    ::-webkit-scrollbar {
        display: none; !* Chrome Safari *!
    }*/
    .vm-dialog-div{
        height: 100%;
    }
    .row_lineheight{
        line-height: 22px;
    }
    .bluecolor{
        color: #66b1ff;
        padding-left: 5px;
    }
</style>

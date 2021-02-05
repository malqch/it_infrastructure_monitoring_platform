<template>
    <div>
<!--        <div class="wrapper">-->
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 网络设备
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="searchData">
                <el-row class="margin_bot">
                    <el-row type="flex" class="row-bg" justify="space-around">
                        <el-col style="margin-bottom: 20px;">
                            <el-button
                                    type="primary"
                                    icon="el-icon-edit"
                                    @click="handleCreate()"
                                    class="handle-box"
                                    plain
                            >增加
                            </el-button>
                            <el-button @click="exportData" type="danger" plain>导出Excel
                            </el-button>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="2">
                            <el-button class="mr10" @click="exportTemplate" type="info" plain>下载模版
                            </el-button>
                        </el-col>
                        <el-col :span="18">
                            <el-upload
                                    class="upload-demo inlineB"
                                    ref="uploadExcel"
                                    :action="excelUrl"
                                    :headers="headers"
                                    :limit="1"
                                    :auto-upload="false"
                                    :on-success="uploadSuccess"
                                    :on-error="handleError"
                            >
                                <el-button class="mr10" slot="trigger" size="small" type="warning" plain>选取文件</el-button>
                                <el-button style="margin-left: 10px;" size="small" type="success" plain @click="importExcel">上传到服务器</el-button>
                                <div slot="tip" class="el-upload__tip"></div>
                            </el-upload>
                        </el-col>
                    </el-row>
                </el-row>
                <div type="flex" class="row-bg" justify="end">
                    <el-form-item>
                        <el-input v-model="searchData.ipaddr" clearable placeholder="ip" class="handle-input"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="searchData.name" clearable placeholder="名称" class="handle-input"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-select v-model="searchData.asset_manager" placeholder="资产管理者" @focus="queryStaff" clearable>
                            <el-option
                                    v-for="item in assetStaffData"
                                    :key="item.id"
                                    :label="item.username"
                                    :value="item.id">
                            </el-option>
                        </el-select>
                    </el-form-item>
                    <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                </div>
            </el-form>
            <el-table
                    v-loading="loading"
                    :data="tableData"
                    border
                    style="width: 100%">
                <el-table-column type="index" label="序号" align="center"></el-table-column>
                <af-table-column prop="name" label="名称" align="center"></af-table-column>
                <af-table-column prop="ipaddr" label="ip地址" align="center"></af-table-column>
<!--                    <el-table-column prop="macaddr" label="mac地址" align="center"></el-table-column>-->
                <af-table-column prop="manufacture" label="供应商" align="center"></af-table-column>
                <af-table-column prop="type" label="类型" align="center"></af-table-column>
                <af-table-column prop="belong_business" label="所属业务" align="center">
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchBusiness(scope.row)" class="color-link">查看业务</el-link>
                    </template>
                </af-table-column>
                <af-table-column prop="label" label="标签" align="center">
                    <template slot-scope="scope">
                        <el-link type="info" @click="searchLabel(scope.row)" class="color-link">查看标签</el-link>
                    </template>
                </af-table-column>
                <af-table-column prop="is_monitor" label="是否监控" align="center"></af-table-column>
                <af-table-column prop="data_center" label="数据中心" align="center" :formatter="handleDataCenter"></af-table-column>
                <af-table-column prop="location_zone" label="机房" align="center" :formatter="handleRoom"></af-table-column>
                <af-table-column prop="location_cabinet" label="机柜" align="center" :formatter="handleRack"></af-table-column>
                <af-table-column prop="device_start_unit" label="起始高度" align="center"></af-table-column>
                <af-table-column prop="device_unit" label="高度(U)" align="center"></af-table-column>
                <af-table-column prop="manage_address" label="管理地址" align="center"></af-table-column>
                <af-table-column prop="manage_username" label="管理用户名" align="center"></af-table-column>
                <af-table-column prop="snmp_username" label="snmp用户名" align="center"></af-table-column>
                <af-table-column prop="snmp_version" label="snmp版本" align="center"></af-table-column>
                <af-table-column prop="device_arrived_date" label="服务开始时间" align="center"></af-table-column>
                <af-table-column prop="device_expire_date" label="服务结束时间" align="center"></af-table-column>
                <el-table-column prop="desc" label="描述" align="center"></el-table-column>
                <af-table-column prop="asset_manager.username" label="资产管理者" align="center"></af-table-column>
                <el-table-column fixed="right" label="操作"  align="center" width="150px">
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
                                style="color: red"
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
<!--                </div>-->
            </div>

            <!-- 新增弹出框 -->
            <el-dialog title="添加设备" :visible.sync="createVisible" width="50%">
                <el-form ref="form" :rules="rules" :model="form" class="demo-ruleForm" label-width="100px">
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="名称" prop="name">
                                <el-input v-model="form.name"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="MAC地址" prop="macaddr">
                                <el-input v-model="form.macaddr"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="IP地址" prop="ipaddr">
                                <el-input v-model="form.ipaddr"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="主机名称" prop="hostname">
                                <el-input v-model="form.hostname"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="厂商">
                                <el-select style="width:100%" value-key="id"  v-model="form.manufacture" placeholder="请选择厂商" @focus="queryvendor" clearable>
                                    <el-option v-for="item in vendorData"
                                               :key=item.vendor_name
                                               :label="item.vendor_name"
                                               :value=item.vendor_name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="类型" prop="type">
                                <el-select style="width: 100%" v-model="form.type" placeholder="请选择类型">
                                    <el-option value="Switch"></el-option>
                                    <el-option value="FW"></el-option>
                                    <el-option value="LB"></el-option>
                                    <el-option value="Router"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="数据中心" prop="data_center">
                                <el-select style="width:100%" value-key="dc_name"  v-model="form.data_center" placeholder="请选择数据中心" @focus="querydatacenter" clearable>
                                    <el-option v-for="item in datacenterData"
                                               :key=item.dc_name
                                               :label="item.dc_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="机房" prop="location_zone">
                                <el-select style="width:100%" value-key="id"  v-model="form.location_zone" placeholder="请选择机房" @focus="addqueryroom" clearable>
                                    <el-option v-for="item in roomData"
                                               :key=item.id
                                               :label="item.room_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="机柜" prop="location_cabinet">
                                <el-select style="width:100%" value-key="id"  v-model="form.location_cabinet" placeholder="请选择机柜" @focus="addqueryrack" clearable>
                                    <el-option v-for="item in rackData"
                                               :key=item.id
                                               :label="item.rack_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="sn" prop="device_sn">
                                <el-input v-model="form.device_sn"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="内存容量" prop="memory_capacity">
                                <el-input type="number" v-model.number="form.memory_capacity"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item  label="磁盘容量" prop="disk_capacity">
                                <el-input type="number" v-model.number="form.disk_capacity"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="cpu型号">
                                <el-input v-model="form.cpu_model"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="cpu核数">
                                <el-input v-model="form.cpu_cores"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="系列" prop="type">
                                <el-select style="width:100%" value-key="id"  v-model="form.series" placeholder="请选择系列" @focus="queryseries" clearable>
                                    <el-option v-for="item in seriesData"
                                               :key=item.id
                                               :label="item.series_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="描述">
                                <el-input v-model="form.desc"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="型号">
                                <el-input v-model="form.model"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="起始高度">
                                <el-input v-model="form.device_start_unit"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="高度(U)">
                                <el-input v-model="form.device_unit"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="管理地址">
                                <el-input v-model="form.manage_address"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="管理用户名">
                                <el-input v-model="form.manage_username"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="管理密码">
                                <el-input v-model="form.manage_password"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="snmp用户名">
                                <el-input v-model="form.snmp_username"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="snmp密码">
                                <el-input v-model="form.snmp_password"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="snmp版本">
                                <el-select style="width:100%" v-model="form.snmp_version" placeholder="请选择类型" clearable>
                                    <el-option
                                            v-for="item in snmpVersionOptions"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="操作系统">
                                <el-select style="width:100%" v-model="form.operate_system" placeholder="请选择操作系统" clearable>
                                    <el-option
                                            v-for="item in operatesystemOptions"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="操作系统版本">
                                <el-input v-model="form.system_version"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="用途">
                                <el-input v-model="form.usage"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="所属业务">
                                <el-select style="width:100%" value-key="id"  v-model="form.belong_business" placeholder="请选择所属业务" @focus="querybusiness()" multiple>
                                    <el-option v-for="item in businessData"
                                               :key=item.id
                                               :label="item.name"
                                               :value=item.name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="标签">
                                <el-select style="width:100%" value-key="id"  v-model="form.label" placeholder="请选择标签" @focus="querylabel" multiple>
                                    <el-option v-for="item in labelData"
                                               :key=item.id
                                               :label="item.tag_name"
                                               :value=item.tag_name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="开始时间">
                                <el-date-picker
                                        v-model="form.device_arrived_date"
                                        type="date"
                                        placeholder="选择日期"
                                        :editable="false"
                                        style="width:100%"
                                        value-format=yyyy-MM-dd>
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                                <el-date-picker
                                        v-model="form.device_expire_date"
                                        type="date"
                                        placeholder="选择日期"
                                        :editable="false"
                                        style="width: 100%"
                                        value-format=yyyy-MM-dd>
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="是否监控">
                                <el-select style="width:100%" v-model="form.is_monitor" placeholder="请选择" clearable>
                                    <el-option
                                            v-for="item in is_monitor_options"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="资产管理者">
                                <el-select style="width:100%" v-model="form.asset_manager" placeholder="请选择" @focus="queryStaff" clearable>
                                    <el-option
                                            v-for="item in assetStaffData"
                                            :key="item.id"
                                            :label="item.username"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetCreate">取 消</el-button>
                <el-button type="primary" @click="saveCreate">确 定</el-button>
            </span>
            </el-dialog>

            <!-- 编辑弹出框 -->
            <el-dialog title="修改设备" :visible.sync="editVisible" width="50%">
                <el-form ref="edit_form" :rules="rules" :model="edit_form" class="demo-ruleForm" label-width="100px">
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="名称" prop="name">
                                <el-input v-model="edit_form.name"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="MAC地址" prop="macaddr">
                                <el-input v-model="edit_form.macaddr"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="IP地址" prop="ipaddr">
                                <el-input v-model="edit_form.ipaddr"></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="主机名称" prop="hostname">
                                <el-input v-model="edit_form.hostname"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="厂商">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.manufacture" placeholder="请选择厂商" @focus="queryvendor" clearable>
                                    <el-option v-for="item in vendorData"
                                               :key=item.vendor_name
                                               :label="item.vendor_name"
                                               :value=item.vendor_name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="类型" prop="type">
                                <el-select style="width: 100%" v-model="edit_form.type" placeholder="请选择类型">
                                    <el-option value="Switch"></el-option>
                                    <el-option value="FW"></el-option>
                                    <el-option value="LB"></el-option>
                                    <el-option value="Router"></el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="数据中心" prop="data_center">
                                <el-select style="width:100%" value-key="dc_name"  v-model="edit_form.data_center" placeholder="请选择数据中心" @focus="querydatacenter">
                                    <el-option v-for="item in datacenterData"
                                               :key=item.dc_name
                                               :label="item.dc_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="机房" prop="location_zone">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.location_zone" placeholder="请选择机房" @focus="editqueryroom">
                                    <el-option v-for="item in roomData"
                                               :key=item.id
                                               :label="item.room_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="机柜" prop="location_cabinet">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.location_cabinet" placeholder="请选择机柜" @focus="editqueryrack">
                                    <el-option v-for="item in rackData"
                                               :key=item.id
                                               :label="item.rack_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="sn" prop="device_sn">
                                <el-input v-model="edit_form.device_sn"></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="内存容量" prop="memory_capacity">
                                <el-input type="number" v-model.number="edit_form.memory_capacity" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item  label="磁盘容量" prop="disk_capacity">
                                <el-input type="number" v-model.number="edit_form.disk_capacity" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="cpu型号">
                                <el-input v-model="edit_form.cpu_model" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="cpu核数">
                                <el-input v-model="edit_form.cpu_cores" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="系列" prop="type">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.series" placeholder="请选择系列" @focus="queryseries" clearable>
                                    <el-option v-for="item in seriesData"
                                               :key=item.id
                                               :label="item.series_name"
                                               :value=item.id>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="描述">
                                <el-input v-model="edit_form.desc" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="型号">
                                <el-input v-model="edit_form.model" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="起始高度">
                                <el-input v-model="edit_form.device_start_unit" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="高度(U)">
                                <el-input v-model="edit_form.device_unit" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="管理地址">
                                <el-input v-model="edit_form.manage_address" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="管理用户名">
                                <el-input v-model="edit_form.manage_username" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="管理密码">
                                <el-input v-model="edit_form.manage_password" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="snmp用户名">
                                <el-input v-model="edit_form.snmp_username" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="snmp密码">
                                <el-input v-model="edit_form.snmp_password" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="snmp版本">
                                <el-select style="width:100%" v-model="edit_form.snmp_version" placeholder="请选择类型" >
                                    <el-option
                                            v-for="item in snmpVersionOptions"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="操作系统">
                                <el-select style="width:100%" v-model="edit_form.operate_system" placeholder="请选择操作系统" clearable>
                                    <el-option
                                            v-for="item in operatesystemOptions"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="操作系统版本">
                                <el-input v-model="edit_form.system_version" clearable></el-input>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="用途">
                                <el-input v-model="edit_form.usage" clearable></el-input>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="所属业务">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.belong_business" placeholder="请选择所属业务" @focus="querybusiness()" multiple>
                                    <el-option v-for="item in businessData"
                                               :key=item.id
                                               :label="item.name"
                                               :value=item.name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="标签">
                                <el-select style="width:100%" value-key="id"  v-model="edit_form.label" placeholder="请选择标签" @focus="querylabel" multiple>
                                    <el-option v-for="item in labelData"
                                               :key=item.id
                                               :label="item.tag_name"
                                               :value=item.tag_name>
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="开始时间">
                                <el-date-picker
                                        v-model="edit_form.device_arrived_date"
                                        type="date"
                                        placeholder="选择日期"
                                        :editable="false"
                                        style="width:100%"
                                        value-format=yyyy-MM-dd>
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="结束时间">
                                <el-date-picker
                                        v-model="edit_form.device_expire_date"
                                        type="date"
                                        placeholder="选择日期"
                                        :editable="false"
                                        style="width: 100%"
                                        value-format=yyyy-MM-dd>
                                </el-date-picker>
                            </el-form-item>
                        </el-col>
                    </el-row>
                    <el-row>
                        <el-col :span="12">
                            <el-form-item label="是否监控">
                                <el-select style="width:100%" v-model="edit_form.is_monitor" placeholder="请选择" clearable>
                                    <el-option
                                            v-for="item in is_monitor_options"
                                            :key="item.value"
                                            :label="item.value"
                                            :value="item.value">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                        <el-col :span="12">
                            <el-form-item label="资产管理者">
                                <el-select style="width:100%" v-model="edit_form.asset_manager" placeholder="请选择" @focus="queryStaff" clearable>
                                    <el-option
                                            v-for="item in assetStaffData"
                                            :key="item.id"
                                            :label="item.username"
                                            :value="item.id">
                                    </el-option>
                                </el-select>
                            </el-form-item>
                        </el-col>
                    </el-row>
                </el-form>
                <span slot="footer" class="dialog-footer">
                <el-button @click="resetEdit">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
            </el-dialog>

            <el-dialog title="所属业务" :visible.sync="businessVisible" width="30%" class="alert_dialog">
                <ul :model="businessSingleDATA[0]" v-for="item in businessSingleDATA" :key="item.id" class="network_ul">
                    <li>
                        <em class="network_ang"></em>
                        <label class="network_label">业务名称:</label>
                        <span class="network_span">{{item.name}}</span>
                    </li>
                    <li>
                        <em class="network_ang"></em>
                        <label class="network_label">业务负责人:</label>
                        <span class="network_span">{{item.staff.username}}</span>
                    </li>
                    <li>
                        <em class="network_ang"></em>
                        <label class="network_label">邮箱:</label>
                        <span class="network_span">{{item.staff.email}}</span>
                    </li>
                    <li>
                        <em class="network_ang"></em>
                        <label class="network_label">电话:</label>
                        <span class="network_span">{{item.staff.phone}}</span>
                    </li>
                </ul>
            </el-dialog>
            <el-dialog title="标签" :visible.sync="labelVisible" width="30%" class="alert_dialog">
                <ul :model="labelSingleData[0]" v-for="item in labelSingleData" :key="item.id" class="network_ul">
                    <li>
                        <em class="network_ang"></em>
                        <label class="network_label">标签名称:</label>
                        <span class="network_span">{{item.tag_name}}</span>
                    </li>
                </ul>
            </el-dialog>
        </div>
    </div>
</template>

<script>
    // import { validateCh } from "@/util/validate";
    import {validateIP} from "../../../util/validate";
    export default {
        name: "Firewall",
        data() {
            return{
                tableData: [],
                vendorData: [],
                datacenterData: [],
                roomData: [],
                rackData: [],
                businessData: [],
                businessSingleDATA: [{
                    name: "",
                    email: "",
                    staff:{"username":"", "email": "", "phone":""}
                }],
                businessVisible: false,
                labelData: [],
                labelSingleData:[],
                departmentData:[],
                labelVisible: false,
                seriesData: [],
                assetStaffData: [],
                searchData: {
                    ipaddr: "",
                    name: "",
                    type: ["FW", "Switch", "Router", "LB"],
                    asset_manager: ""
                },
                headers:{
                    'token': localStorage.getItem('token')
                },
                excelUrl: 'asset/api/nro/network/excel/',
                rules: {
                    name: [
                        {required: true, message: '请输入名称'},
                        { trigger: 'blur'},
                    ],
                    snmp_username: [
                        {required: false, message: '请输入名称'},
                        {trigger: 'blur'}
                    ],
                    ipaddr: [
                        {required: true, message: '请输入IP地址'},
                        {trigger: 'blur', validator: validateIP}
                    ],
                    type: [
                        {required: true, message: '请输入类型'},
                        {trigger: 'blur'}
                    ],
                    // model: [
                    //     {required: true, message: '请输入型号'},
                    //     {trigger: 'blur'}
                    // ],
                    // version: [
                    //     {required: true, message: '请输入版本号'},
                    //     {trigger: 'blur'}
                    // ],
                    manufacture: [
                        {required: true, message: '请输入厂商'},
                        {trigger: 'blur'}
                    ],
                    data_center: [
                        { required: true, message: '请选择数据中心', trigger: 'input'}
                    ],
                    location_zone: [
                        { required: true, message: '请选择机房', trigger: 'input'}
                    ],
                    memory_capacity: [
                        { required: false, message: '请输入内存容量', trigger: 'blur'}
                    ],
                    disk_capacity: [
                        { required: false, message: '请输入磁盘容量', trigger: 'blur'}
                    ],
                    series: [
                        { required: true, message: '请选择系列' },
                        { trigger: 'blur'}
                    ],
                    location_cabinet: [
                        { required: true, message: '请选择机柜', trigger: 'input'}
                    ],
                    device_sn: [
                        { required: true, message: '请输入sn', trigger: 'input'}
                    ]
                },
                is_monitor_options:[{
                    value: "是"
                },{
                    value: "否"
                }],
                snmpVersionOptions:[{
                    value: 1
                }, {
                    value: 2
                }, {
                    value: 3
                }],
                operatesystemOptions: [{
                    value: 'Windows'
                },{
                    value: 'Neokylin'
                },{
                    value: 'SUSE'
                }, {
                    value: 'RedHat'
                }, {
                    value: 'Centos'
                }, {
                    value: 'Ubuntu'
                }
                ],
                pageTotal: 0,
                query: {
                    address: '',
                    name: '',
                    pageIndex: 1,
                    pageSize: 10
                },
                form: {
                    "dgid": '无',
                },
                edit_form: {
                    "manage_password": '',
                    "snmp_password": ''
                },
                datacenterid: "", //编辑时保存id使用
                roomid : "",
                rackid: '',
                seriesid: '',
                asset_manager_id: '',
                dc_name: '',
                room_name: '',
                rack_name: '',
                createVisible: false,
                editVisible: false,
                loading: true
            }
        },
        created() {
            this.getData()
        },
        methods: {
            getData() {
                this.$http.get(`asset/api/nro/network/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&ipaddr=${this.searchData.ipaddr}&name=${
                    this.searchData.name}&asset_manager=${this.searchData.asset_manager}`, {
                    headers:
                        {
                            'token': localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.tableData = res.data['data'];
                    this.pageTotal = res.data['total_count'];
                    this.loading = false
                }).catch( (error) =>{
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
                });
            } ,
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },

            // 创建操作
            handleCreate() {
                this.createVisible = true;
                this.form = {"dgid":'无'};
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 重置新增
            resetCreate() {
                this.createVisible = false;
                this.getData();
                this.form = {"dgid":'无'};
            },

            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.editVisible = true;
                this.edit_form = JSON.parse(JSON.stringify(row));
                this.labelData = row.label
                this.businessData = row.belong_business
                // 为了编辑时选择框显示名称
                if (row.data_center) {
                    this.datacenterid = row.data_center.id
                    this.edit_form.data_center = row.data_center.dc_name
                }
                if (row.location_cabinet) {
                    this.rackid = row.location_cabinet.id
                    this.edit_form.location_cabinet = row.location_cabinet.rack_name
                }
                if (row.location_zone) {
                    this.roomid = row.location_zone.id
                    this.edit_form.location_zone = row.location_zone.room_name
                }
                //编辑时显示系列名称
                if (row.series) {
                    this.seriesid = row.series.id
                    this.edit_form.series = row.series.series_name
                }

                var form_label_name = []
                for (var labelindex in this.labelData) {
                    form_label_name.push(this.labelData[labelindex].tag_name)
                }
                // 将新的Number数组，绑定到select空间的v-model上
                this.edit_form.label = form_label_name

                var form_business_name = []
                for (var businessindex in this.businessData) {
                    form_business_name.push(this.businessData[businessindex].name)
                }

                // 将新的Number数组，绑定到select空间的v-model上
                this.edit_form.belong_business = form_business_name;
                if(row.asset_manager) {
                    this.asset_manager_id  = row.asset_manager.id;
                    this.edit_form.asset_manager = row.asset_manager.username;
                }
            },
            //重置修改
            resetEdit() {
              this.editVisible = false;
              this.getData();
            },
            // 保存编辑
            saveEdit() {
                this.$refs.edit_form.validate().then(res => {
                    console.log(res)
                    if(this.edit_form.data_center && typeof this.edit_form.data_center != "number"){
                        this.$set(this.edit_form, 'data_center', this.datacenterid)
                    }
                    if(this.edit_form.location_zone && typeof this.edit_form.location_zone != "number"){
                        this.$set(this.edit_form, 'location_zone', this.roomid)
                    }
                    if(this.edit_form.location_cabinet && typeof this.edit_form.location_cabinet != "number"){
                        this.$set(this.edit_form, 'location_cabinet', this.rackid)
                    }
                    if(this.edit_form.series && typeof this.edit_form.series != "number"){
                        this.$set(this.edit_form, 'series', this.seriesid)
                    }
                    if(this.edit_form.asset_manager && typeof this.edit_form.asset_manager != "number"){
                        this.$set(this.edit_form, 'asset_manager', this.asset_manager_id)
                    }
                    this.edit_form.location = this.edit_form.data_center
                    this.edit_form.status = 0
                    console.log(this.edit_form,111)
                    this.$http.put(`asset/api/nro/network/${this.id}/`,
                        this.edit_form,
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 200) {
                            this.$message.success('更新成功！');
                            this.editVisible = false;
                            this.getData();
                        } else {
                            this.$message.error('更新失败！');
                        }
                    }).catch( (error) => {
                        console.log(error,111)
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },
            //保存新增
            saveCreate() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.form.location = this.form.data_center;
                    this.form.status = 0;
                    this.$http.post(`asset/api/nro/network/`,
                        this.form,
                        {
                            headers: {
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                        if (res.status === 201) {
                            this.$message.success('创建成功！');
                            this.createVisible = false;
                            this.form = {"dgid":'无'};
                            this.getData()
                        } else {
                            this.$message.error('创建失败！');
                            this.form = {"dgid":'无'}
                        }
                    }).catch( (error) => {
                        this.$message.error(JSON.stringify(error.response.data));
                    });
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },

            //查询厂商
            queryvendor() {
                this.$http.get(`asset/api/vendor/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.vendorData = res.data
                });
            },

            //查询数据中心
            querydatacenter() {
                this.$set(this.form, 'location_zone', '')
                this.$set(this.form, 'location_cabinet', '')
                this.$set(this.edit_form, 'location_zone', '')
                this.$set(this.edit_form, 'location_cabinet', '')
                this.$http.get('asset/api/datacenter/?is_delete=0', {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.datacenterData=res.data
                    console.log(this.datacenterData, 5555, typeof this.datacenterData)
                });
            },

            //修改时查询业务信息
            editqueryroom() {
                this.edit_form.location_cabinet = '';
                if(typeof this.edit_form.data_center==="number"){
                    for (let i in this.datacenterData) {
                        if (this.datacenterData[i].id === this.edit_form.data_center) {
                            this.dc_name = this.datacenterData[i].dc_name;
                        }
                    }
                }else {
                    this.dc_name = this.edit_form.data_center;
                }
                this.$http.get(`asset/api/room/?dc_name=${this.dc_name}`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                    console.log(res)
                    this.roomData = res.data
                    console.log(this.roomData,111)
                })
            },
            //新增时查询业务信息
            addqueryroom() {
                for (let i in this.datacenterData) {
                    if (this.datacenterData[i].id === this.form.data_center) {
                        this.dc_name = this.datacenterData[i].dc_name;
                    }
                }
                this.$http.get(`asset/api/room/?dc_name=${this.dc_name}`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                    this.roomData = res.data;
                })
            },
            //新增时查询机房对应机柜
            addqueryrack() {
                if(typeof this.form.location_zone==="number"){
                    for (let i in this.roomData) {
                        if (this.roomData[i].id === this.form.location_zone) {
                            this.room_name = this.roomData[i].room_name
                        }
                    }
                }else {
                    this.room_name = this.form.location_zone
                }
                this.$http.get(`asset/api/rack/rack/?room_name=${this.room_name}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.rackData = res.data
                });
            },

            //修改时查询机房对应机柜
            editqueryrack() {
                if(typeof this.edit_form.location_zone==="number"){
                    for (let i in this.roomData) {
                        if (this.roomData[i].id === this.edit_form.location_zone) {
                            this.room_name = this.roomData[i].room_name
                        }
                    }
                }else {
                    this.room_name = this.edit_form.location_zone
                }
                this.$http.get(`asset/api/rack/rack/?room_name=${this.room_name}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.rackData = res.data
                });
            },

            // 查询系列表
            queryseries(){
                this.$http.get(`asset/api/series/`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.seriesData = res.data;
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },

            //查询业务信息
            querybusiness() {
                this.$http.get(`asset/api/business/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.businessData = res.data
                })
            },

            // 查询标签数据
            querylabel() {
                this.$http.get(`asset/api/tag/`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.labelData = res.data
                    // this.labelSelectData = []
                    console.log(this.labelData)
                });
            },

            // 查询业务
            searchBusiness(row) {
                if(row.belong_business!=""){
                    console.log(row.belong_business,123)
                    this.businessSingleDATA = row.belong_business
                    // for (var p in this.businessSingleDATA) {//遍历json数组时，这么写p为索引，0,1
                    //     if(this.businessSingleDATA[p].staff==null){
                    //         this.businessSingleDATA[p].staff = {"username":"", "email": "", "phone":""}
                    //     }
                    // }
                    this.businessVisible = true
                }else{
                    this.$message.warning('业务信息不存在');
                }
            },

            //查看标签
            searchLabel(row) {
                if(row.label!=''){
                    this.labelSingleData = row.label
                    this.labelVisible = true
                }else{
                    this.$message.warning('标签信息不存在');
                }
            },
            queryStaff() {
                this.$http.get(`asset/api/staff/`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.assetStaffData = res.data;
                    console.log(res.data)
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 处理数据中心
            handleDataCenter(row){
                if(row.data_center){
                    return row.data_center.dc_name
                }else{
                    return ''
                }
            },

            // 处理机房
            handleRoom(row){
                if(row.location_zone){
                    return row.location_zone.room_name
                }else{
                    return ''
                }
            },
            // 处理机柜
            handleRack(row){
                if(row.location_cabinet){
                    return row.location_cabinet.rack_name
                }else{
                    return ''
                }
            },
            //处理系列
            handleSeries(row){
                if(row.series){
                    return row.series.series_name
                }else{
                    return ''
                }
            },
            // 删除操作
            handleDelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.put(`asset/api/nro/network/${row.id}/delete/`,
                    {
                        headers: {
                            'token': localStorage.getItem('token')
                        }
                    }).then((res) => {
                        console.log(res.status,123)
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    } else {
                        this.$message.error(res.data.msg);
                        this.$set(this.query, 'pageIndex',1)
                        this.getData()
                    }

                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},

            // 导出模版
            exportTemplate() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["名称", "ip","sn", "状态","型号","起始高度","高度(U)",
                        "用途","管理用户名","管理密码","管理地址","snmp用户名","snmp密码", "主机名称","操作系统","系统版本","cpu型号",
                        "cpu核数","内存容量","磁盘容量", "服务开始时间", "服务结束时间"];// 上面设置Excel的表格第一行的标题

                    const list = []
                    export_json_to_excel(tHeader, list, "网络设备导入模版");   //标题，数据，文件名
                });
            },
            // 导出数据
            exportData() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["名称", "ip","sn", "状态","型号","起始高度","高度(U)",
                        "用途","管理用户名","管理密码","管理地址","snmp用户名","snmp密码", "主机名称","操作系统","系统版本","cpu型号",
                        "cpu核数","内存容量","磁盘容量", "服务开始时间", "服务结束时间", "资产管理者"];// 上面设置Excel的表格第一行的标题

                    const filterVal = ["name", "ipaddr","device_sn", "status","model", "device_start_unit", "device_unit",
                        "usage", "manage_username", "manage_password", "manage_address", "snmp_username", "snmp_password", "hostname",
                        "operate_system", "system_version", "cpu_model", "cpu_cores", "memory_capacity", "disk_capacity",
                        "device_arrived_date", "device_expire_date", "asset_manager"]; // 上面的index、nickName、name是tableData里对象的属性

                    this.$http.get( `asset/api/nro/network/?ipaddr=${this.searchData.ipaddr}&name=${
                        this.searchData.name}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.exportDataRes = res.data;
                    }).then(() =>{
                        const list = this.exportDataRes;              //把data里的tableData存到list
                        const data = this.formatJson(filterVal, list);

                        export_json_to_excel(tHeader, data, "网络设备");   //标题，数据，文件名
                    })});
            },

            formatJson(filterVal, jsonData) {
                const data_list = []
                jsonData.map((v) => {
                    if(v.asset_manager!=null){
                        v.asset_manager = v.asset_manager.username
                    }
                    const res = filterVal.map(j => v[j])
                    data_list.push(res)
                });
                return data_list
            },
            // 导入excel
            importExcel() {
                if(this.$refs.uploadExcel.uploadFiles.length===0){
                    this.$message.error("请选取文件")
                }else{
                    this.$refs.uploadExcel.submit();
                }
            },
            //excel上传成功时
            uploadSuccess(file){
                console.log(file);
                this.$refs.uploadExcel.clearFiles();
                this.getData()
                alert('上传成功！');
            },
            handleError(err){
                const msg = JSON.parse(err.message)
                console.log(msg.msg)
                alert(msg.msg)
            },
        }
    }
</script>

<style lang="scss" scoped>
    @import "../../../assets/scss/serve.scss";
    .margin_bot{
        margin-bottom: 10px;
    }
</style>

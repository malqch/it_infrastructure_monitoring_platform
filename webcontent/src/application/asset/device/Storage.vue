<template>
    <div>
        <div class="crumbs">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>
                    <i class="el-icon-lx-cascades"></i> 存储
                </el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <div class="container">
            <el-form :inline="true" v-model="searchData">
                <el-row class="margin_bot">
                    <el-row type="flex" class="row-bg" justify="space-around">
                        <el-col>
                            <el-button
                                    type="primary"
                                    icon="el-icon-edit"
                                    @click="handleAdd()"
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
                                    :on-error="handleError">
                                <el-button class="mr10" slot="trigger" size="small" type="warning" plain>选取文件</el-button>
                                <el-button size="small" type="success" plain @click="importExcel">上传到服务器</el-button>
                                <div slot="tip" class="el-upload__tip"></div>
                            </el-upload>
                        </el-col>
                    </el-row>
                </el-row>
                <el-row>
                   <el-col :span="30" :inline="true">
<!--                       <el-form-item>-->
<!--                           <el-input v-model="searchData.manage_address" placeholder="管理ip" class="handle-input"></el-input>-->
<!--                       </el-form-item>-->
                       <el-form-item>
                           <el-input v-model="searchData.storage_name" placeholder="名称" class="handle-input" clearable></el-input>
                       </el-form-item>
                       <el-form-item>
                           <el-input v-model="searchData.hostname" placeholder="主机名" class="handle-input" clearable></el-input>
                       </el-form-item>
                       <el-form-item>
                           <el-select style="width:100%" value-key="id"  v-model="searchData.vendor" placeholder="请选择厂商" @focus="queryvendor" clearable>
                               <el-option v-for="item in vendorData"
                                          :key=item.id
                                          :label="item.vendor_name"
                                          :value=item.id>
                               </el-option>
                           </el-select>
                       </el-form-item>
                       <el-form-item>
                           <el-select v-model="searchData.asset_manager" placeholder="资产管理者" clearable>
                               <el-option
                                       v-for="item in assetStaffData"
                                       :key="item.id"
                                       :label="item.username"
                                       :value="item.id">
                               </el-option>
                           </el-select>
                       </el-form-item>
                   </el-col>
                   <el-button icon="el-icon-search" type="primary" class="handle-box" @click="handleSearch">查询</el-button>
                </el-row>
            </el-form>
           <el-table
                   v-loading="loading"
                :data="tableData"
                border
                style="width: 100%"
           >
<!--            <el-table-column fixed width="50" type="selection" align="center"></el-table-column>-->
               <el-table-column width="50" type="index" label="序号" align="center"></el-table-column>
               <af-table-column prop="storage_name" label="名称" align="center"></af-table-column>
               <af-table-column prop="hostname" label="主机名" align="center"></af-table-column>
               <!--<af-table-column prop="sn" label=" sn " align="center"></af-table-column>-->
               <af-table-column prop="vendor" label="供应商" align="center" :formatter="handleVendor"></af-table-column>
               <af-table-column prop="series" label="系列" align="center" :formatter="handleSeries"></af-table-column>
               <af-table-column prop="storage_model" label="型号" align="center"></af-table-column>
               <af-table-column prop="is_monitor" label="是否监控" align="center"></af-table-column>
               <af-table-column prop="data_center" label="数据中心" align="center" :formatter="handleDataCenter"></af-table-column>
               <af-table-column prop="location_zone" label="机房" align="center" :formatter="handleRoom"></af-table-column>
               <af-table-column prop="location_cabinet" label="机柜" align="center" :formatter="handleRack"></af-table-column>
               <af-table-column prop="manage_address" label="管理地址" align="center"></af-table-column>
               <af-table-column prop="manage_username" label="管理名称" align="center"></af-table-column>
<!--               <af-table-column prop="manage_password" label="管理密码" align="center"></af-table-column>-->
               <af-table-column prop="storage_start_unit" label="起始高度" align="center"></af-table-column>
               <af-table-column prop="storage_unit" label="高度(U)" align="center"></af-table-column>
               <af-table-column prop="label" label="标签" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchLabel(scope.row)" class="color-link">查看标签</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="server_belong_business" label="所属业务" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchBusiness(scope.row)" class="color-link">查看业务</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="network" label="网卡信息" align="center">
                   <template slot-scope="scope">
                       <el-link type="info" @click="searchNetwork(scope.row)" class="color-link">查看网卡信息</el-link>
                   </template>
               </af-table-column>
               <af-table-column prop="usage" label="用途" align="center"></af-table-column>
               <af-table-column prop="disk_capacity" label="磁盘容量" align="center"></af-table-column>
               <af-table-column prop="disk_model" label="磁盘型号" align="center"></af-table-column>
               <af-table-column prop="disk_vendor" label="磁盘厂商" align="center" :formatter="handleDiskVendor"></af-table-column>
               <af-table-column prop="controller_num" label="控制器数量" align="center"></af-table-column>
               <af-table-column prop="controller_system_version" label="控制器系统版本" align="center"></af-table-column>
               <af-table-column prop="host_port_type" label="主机端口类型" align="center"></af-table-column>
               <af-table-column prop="host_port_num" label="主机端口数量" align="center"></af-table-column>
               <af-table-column prop="extension_port_type" label="扩展端口类型" align="center"></af-table-column>
               <af-table-column prop="extension_port_num" label="扩展端口数量" align="center"></af-table-column>
               <af-table-column prop="extension_rack_type" label="扩展柜类型" align="center"></af-table-column>
               <af-table-column prop="extension_rack_num" label="扩展柜数量" align="center"></af-table-column>
               <af-table-column prop="controller_rack_disk_num" label="控制柜硬盘数量" align="center"></af-table-column>
               <af-table-column prop="extension_rack_disk_num" label="扩展柜硬盘数量" align="center"></af-table-column>
               <af-table-column prop="arrived_date" label="服务开始时间" align="center"></af-table-column>
               <af-table-column prop="expire_date" label="服务结束时间" align="center"></af-table-column>
               <af-table-column prop="update_time" label="更新时间" align="center" :formatter="dateFormat"></af-table-column>
               <af-table-column prop="asset_manager.username" label="资产管理者" align="center"></af-table-column>
               <el-table-column fixed="right" label="操作" width="150" align="center">
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
                        class="red"
                        @click="handledelete(scope.row)"
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
        <el-dialog :title="makeTitle" :visible.sync="editVisible" width="50%">
            <el-form ref="form" :rules="rules" :model="form" label-width="120px" class="demo-ruleForm">
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="名称" prop="storage_name">
                            <el-input v-model="form.storage_name"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="主机名" prop="hostname">
                            <el-input v-model="form.hostname"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="管理地址" prop="manage_address">
                            <el-input v-model="form.manage_address"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="管理IP" prop="manage_ip">
                            <el-input v-model="form.manage_ip"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="管理名称">
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
                            <el-select style="width:100%" value-key="id"  v-model="form.location_zone" placeholder="请选择机房" @focus="queryroom" clearable>
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
                            <el-select style="width:100%" value-key="id"  v-model="form.location_cabinet" placeholder="请选择机柜" @focus="queryrack" clearable>
                                <el-option v-for="item in rackData"
                                           :key=item.id
                                           :label="item.rack_name"
                                           :value=item.id>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="sn">
                            <el-input v-model="form.sn"></el-input>
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
                        <el-form-item label="厂商">
                            <el-select style="width:100%" value-key="id"  v-model="form.vendor" placeholder="请选择厂商" @focus="queryvendor" clearable>
                                <el-option v-for="item in vendorData"
                                           :key=item.id
                                           :label="item.vendor_name"
                                           :value=item.id>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="系列">
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
                        <el-form-item label="型号">
                            <el-input v-model="form.storage_model"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="起始高度">
                            <el-input v-model="form.storage_start_unit"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="高度">
                            <el-input v-model="form.storage_unit"></el-input>
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
                        <el-form-item label="用途">
                            <el-input v-model="form.usage"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="磁盘型号">
                            <el-input v-model="form.disk_model"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="磁盘容量">
                            <el-input type="number" v-model.number="form.disk_capacity"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="磁盘厂商">
                            <el-select style="width:100%" value-key="id"  v-model="form.disk_vendor" placeholder="请选择厂商" @focus="queryvendor" clearable>
                                <el-option v-for="item in vendorData"
                                           :key=item.id
                                           :label="item.vendor_name"
                                           :value=item.id>
                                </el-option>
                            </el-select>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="控制器系统版本">
                            <el-input v-model="form.controller_system_version"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="控制器数量">
                            <el-input type="number" v-model.number="form.controller_num"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="主机端口类型">
                            <el-input v-model="form.host_port_type"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="主机端口数量">
                            <el-input type="number" v-model.number="form.host_port_num"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="扩展端口类型">
                            <el-input v-model="form.extension_port_type"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="扩展端口数量">
                            <el-input type="number" v-model.number="form.extension_port_num"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="扩展柜类型">
                            <el-input v-model="form.extension_rack_type"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="扩展柜数量">
                            <el-input type="number" v-model.number="form.extension_rack_num"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="控制柜硬盘数量">
                            <el-input type="number" v-model.number="form.controller_rack_disk_num"></el-input>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="扩展柜硬盘数量">
                            <el-input type="number" v-model.number="form.extension_rack_disk_num"></el-input>
                        </el-form-item>
                    </el-col>
                </el-row>
                <el-row>
                    <el-col :span="12">
                        <el-form-item label="服务开始时间">
                            <el-date-picker
                                    v-model="form.arrived_date"
                                    type="date"
                                    placeholder="选择日期"
                                    :editable="false"
                                    style="width: 100%"
                                    value-format=yyyy-MM-dd>
                            </el-date-picker>
                        </el-form-item>
                    </el-col>
                    <el-col :span="12">
                        <el-form-item label="服务结束时间">
                            <el-date-picker
                                    v-model="form.expire_date"
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
                <el-row>
                    <el-col :span="24">
                        <el-form ref="querynetworkData" :rules="networkrules" :model="querynetworkData[0]" label-width="85px" :hide-required-asterisk="true">
                            <el-form-item label="网卡信息">
                                <el-row :gutter="24">
                                    <el-col :span="18" class="net_bg">
                                        <el-row v-for="(item, index) in querynetworkData" :key="item.id">
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="mac" prop="mac">
                                                    <el-input v-model="querynetworkData[index].mac"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-form-item label="netmask">
                                                    <el-input v-model="querynetworkData[index].netmask"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="ip" prop="ip">
                                                    <el-input v-model="querynetworkData[index].ip"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-form-item label="broadcast">
                                                    <el-input v-model="querynetworkData[index].broadcast"></el-input>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="10" class="net_row">
                                                <el-form-item label="type">
                                                    <el-select v-model="querynetworkData[index].type" clearable>
                                                        <el-option
                                                                v-for="item in networkType"
                                                                :key="item.value"
                                                                :label="item.value"
                                                                :value="item.value">
                                                        </el-option>
                                                    </el-select>
                                                </el-form-item>
                                            </el-col>
                                            <el-col :span="14">
                                                <el-button
                                                        @click="del(index)"
                                                        size="small"
                                                        class="margin_26"
                                                        type="danger" plain
                                                ><i class="el-icon-delete"></i></el-button>
                                            </el-col>
                                        </el-row>
                                    </el-col>
                                    <el-col :span="4">
                                        <el-button
                                                @click="addItem"
                                                size="small"
                                                icon="el-icon-circle-plus"
                                                class="margin_26"
                                                type="primary" plain
                                        ></el-button>
                                    </el-col>
                                </el-row>
                            </el-form-item>
                        </el-form>
                    </el-col>
                </el-row>
            </el-form>
            <span slot="footer" class="dialog-footer">
                <el-button @click="editVisible = false">取 消</el-button>
                <el-button type="primary" @click="saveEdit">确 定</el-button>
            </span>
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
        <el-dialog title="网卡信息" :visible.sync="networkVisible" width="35%" class="alert_dialog">
            <ul :model="querynetworkData[0]" v-for="item in querynetworkData" :key="item.id" class="network_ul">
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">mac:</label>
                    <span class="network_span">{{item.mac}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">netmask:</label>
                    <span class="network_span">{{item.netmask}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">ip:</label>
                    <span class="network_span">{{item.ip}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">broadcast:</label>
                    <span class="network_span">{{item.broadcast}}</span>
                </li>
                <li>
                    <em class="network_ang"></em>
                    <label class="network_label">type:</label>
                    <span class="network_span">{{item.type}}</span>
                </li>
            </ul>
        </el-dialog>
    </div>
</template>

<script>
    import {validateIP, validateMac} from "../../../util/validate";

    export default {
        name: "storage",
        data() {
            return{
                form: {},
                makeTitle: '',
                query: {
                        pageIndex: 1,
                        pageSize: 10
                    },
                pageTotal: 0,
                tableData: [],
                querynetworkData: [{}], // 网卡的信息
                vendorData: [], // 查询的厂商列表
                seriesData: [], // 查询的系列列表
                datacenterData: [],  //查询的数据中心列表
                roomData: [], // 机房的列表
                rackData: [], //机柜的列表
                businessData: [], // 业务的列表
                labelData: [],  // 标签的列表
                editVisible: false,  //编辑弹框
                labelSingleData: [],  //标签弹框中的数据
                labelVisible: false, // 标签弹框默认不展开
                assetStaffData: [],
                datacenterid: "", //编辑时保存id使用
                roomid : "",
                rackid: '',
                seriesid: '',
                vendorid: '',
                diskvendorid: '',
                asset_manager_id: '',
                networkVisible: false,  // 网卡信息弹框默认不显示
                excelUrl: 'asset/api/storage/excel/',
                headers:{
                    'token': localStorage.getItem('token')
                },
                networkType: [{
                    value: "内网"
                },{
                    value: "公网"
                }],
                rules: {
                    hostname: [
                        {required: true, message: '请输入主机名', trigger: 'blur'},
                    ],
                    storage_name: [
                        {required: true, message: '请输入设备名', trigger: 'blur'},
                    ],
                    data_center: [
                        {required: true, message: '请选择数据中心', trigger: 'blur'},
                    ],
                    location_zone: [
                        {required: true, message: '请选择机房', trigger: 'blur'},
                    ],
                    location_cabinet: [
                        {required: true, message: '请选择机柜', trigger: 'blur'},
                    ],
                    manage_ip: [
                        {required: true, message: '请输入管理ip地址'},
                        {validator: validateIP, trigger: 'blur'}
                    ],
                    manage_address: [
                        {required: true, message: '请输入管理地址'},
                    ]
                },
                networkrules: {
                    ip: [
                        {required: true, message: 'ip不能为空'},
                        { validator: validateIP, trigger: 'blur'},
                    ],
                    mac: [
                        {required: true, message: 'mac地址不能为空'},
                        {validator: validateMac, trigger: 'blur'}
                    ]
                }, // 网卡中数据验证
                businessSingleDATA: [],  // 业务中的弹框数据
                businessVisible: false,  //业务弹框默认不展开
                searchData: {
                    manage_address: "",
                    storage_name: "",
                    hostname: '',
                    vendor: '',
                    asset_manager: ''
                },
                snmpVersionOptions:[{
                    value: 1
                }, {
                    value: 2
                }, {
                    value: 3
                }],
                is_monitor_options:[{
                    value: "是"
                },{
                    value: "否"
                }],
                loading: true
            }
        },
        created() {
            this.getData();
        },
        methods: {
            getData() {
                this.$http.get(`asset/api/storage/?current_page=${this.query.pageIndex}&pre_page=${
                    this.query.pageSize}&storage_name=${this.searchData.storage_name}&hostname=${this.searchData.hostname
                }&vendor=${this.searchData.vendor}&manage_address=${this.searchData.manage_address}&asset_manager=${
                    this.searchData.asset_manager}`, {
                    headers: {
                        'token':localStorage.getItem('token')
                    }}).then((res) => {
                        this.tableData = res.data['data']
                        this.pageTotal = res.data['total_count'];
                        this.loading = false;
                }).catch( (error) => {
                    this.$message.error(JSON.stringify(error.response.data));
                    this.loading = false;
                });
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
            //查询数据中心
            querydatacenter() {
                this.$set(this.form, 'location_zone', '')
                this.$set(this.form, 'location_cabinet', '')
                this.$http.get('asset/api/datacenter/?is_delete=0', {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.datacenterData=res.data
                });
            },
            // 查询机房
            queryroom() {
                this.$set(this.form, 'location_cabinet', '')
                let data_center_name = ''
                let data_center_id = ''
                if(typeof this.form.data_center==="number"){
                    data_center_id = this.form.data_center
                }else if(this.form.data_center != null){
                    data_center_name = this.form.data_center
                }
                this.$http.get(`asset/api/room/room/?id=${data_center_id}&dc_name=${data_center_name}&is_delete=0`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.roomData = res.data
                });
            },
            //查询机房对应机柜
            queryrack() {
                let room_name = ''
                let room_id = ''
                if(typeof this.form.location_zone==="number"){
                    room_id = this.form.location_zone
                }else if(this.form.location_zone != null){
                    room_name = this.form.location_zone
                }
                this.$http.get(`asset/api/rack/rack/?room_id=${room_id}&room_name=${room_name}&is_delete=0`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.rackData = res.data
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
                });
            },
            queryStaff() {
                this.$http.get(`asset/api/staff/`, {
                    headers:
                        {
                            'token':localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.assetStaffData = res.data;
                }).catch( (error)=> {
                    this.$message.error(JSON.stringify(error.response.data));
                });
            },
            // 处理厂商
            handleVendor(row){
                if(row.vendor){
                    return row.vendor.vendor_name
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
            //查看标签
            searchLabel(row) {
                if(row.label!=''){
                    this.labelSingleData = row.label
                    this.labelVisible = true
                }else{
                    this.$message.warning('标签信息不存在');
                }
            },
            //查看业务
            searchBusiness(row) {
                if(row.belong_business!=""){
                    this.businessSingleDATA = row.belong_business
                    for (var p in this.businessSingleDATA) {//遍历json数组时，这么写p为索引，0,1
                        if(this.businessSingleDATA[p].staff==null){
                            this.businessSingleDATA[p].staff = {"username":"", "email": "", "phone":""}
                        }
                    }
                    this.businessVisible = true
                }else{
                    this.$message.warning('业务信息不存在');
                }
            },
            handleDiskVendor(row){
                if(row.disk_vendor){
                    return row.disk_vendor.vendor_name
                }else{
                    return ''
                }
            },
            // 编辑操作
            handleEdit(row) {
                this.id = row.id;
                this.makeTitle = "编辑";
                this.form = JSON.parse( JSON.stringify(row));
                this.labelData = row.label
                this.businessData = row.belong_business
                // 为了编辑时选择框显示名称
                if(row.data_center){
                    this.datacenterid = row.data_center.id
                    this.form.data_center = row.data_center.dc_name
                }
                if(row.location_cabinet){
                    this.rackid = row.location_cabinet.id
                    this.form.location_cabinet = row.location_cabinet.rack_name
                }
                if(row.location_zone){
                    this.roomid  = row.location_zone.id
                    this.form.location_zone = row.location_zone.room_name
                }
                //编辑时显示系列名称
                if(row.series){
                    this.seriesid = row.series.id
                    this.form.series = row.series.series_name
                }
                //编辑时显示厂商名称
                if(row.vendor){
                    this.vendorid  = row.vendor.id
                    this.form.vendor = row.vendor.vendor_name
                }
                // 编辑时现实磁盘厂商名称
                if(row.disk_vendor){
                    this.diskvendorid  = row.disk_vendor.id
                    this.form.disk_vendor = row.disk_vendor.vendor_name
                }

                var form_label_name = []
                for (var labelindex in this.labelData) {
                    form_label_name.push(this.labelData[labelindex].tag_name)
                }
                // 将新的Number数组，绑定到select空间的v-model上
                this.form.label = form_label_name

                var form_business_name = []
                for (var businessindex in this.businessData) {
                    form_business_name.push(this.businessData[businessindex].name)
                }

                // 将新的Number数组，绑定到select空间的v-model上
                this.form.belong_business = form_business_name
                if(row.asset_manager) {
                    this.asset_manager_id  = row.asset_manager.id;
                    this.form.asset_manager = row.asset_manager.username;
                }

                this.$http.get(`asset/api/network/networks/?storage_id=${row.id}`, {
                    headers:
                        {
                            'token': localStorage.getItem('token')
                        }
                }).then((res) => {
                    this.querynetworkData = res.data
                });
                this.editVisible = true;
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 保存编辑
            saveEdit() {
                this.$refs.form.validate().then(res => {
                    console.log(res)
                    this.$set(this.form, 'network', this.querynetworkData)
                    if(this.makeTitle=="增加"){
                        this.$http.post(`asset/api/storage/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            if (res.status === 201) {
                                this.editVisible = false
                                console.log('Response:' + JSON.stringify(res));
                                this.$message.success('保存成功！');
                                this.form = {}
                                // this.searchData = {
                                //     device_ip: "",
                                //     device_name: "",
                                //     device_status: "",
                                //     device_vendor: "",
                                //     device_type: "服务器",
                                //     maintain_status: "",
                                //     hostname: ""
                                // }, // 把查询条件设置成空，避免新增数据后还是按条件查询的
                                    this.getData()
                            } else {
                                this.$message.error('保存失败！');
                            }
                        }).catch((error) => {
                            if (error.response.status==409) {
                                this.$message.error(JSON.stringify(error.response.data.msg));
                            }else{
                                this.$message.error(JSON.stringify(error.response.data));
                            }

                        })
                    }else{
                        if(this.form.data_center && typeof this.form.data_center != "number"){
                            this.$set(this.form, 'data_center', this.datacenterid)
                        }
                        if(this.form.location_zone && typeof this.form.location_zone != "number"){
                            this.$set(this.form, 'location_zone', this.roomid)
                        }
                        if(this.form.location_cabinet && typeof this.form.location_cabinet != "number"){
                            this.$set(this.form, 'location_cabinet', this.rackid)
                        }
                        if(this.form.series && typeof this.form.series != "number"){
                            this.$set(this.form, 'series', this.seriesid)
                        }
                        if(this.form.vendor && typeof this.form.vendor != "number"){
                            this.$set(this.form, 'vendor', this.vendorid)
                        }
                        if(this.form.disk_vendor && typeof this.form.disk_vendor != "number"){
                            this.$set(this.form, 'disk_vendor', this.diskvendorid)
                        }
                        if(this.form.asset_manager && typeof this.form.asset_manager != "number"){
                            this.$set(this.form, 'asset_manager', this.asset_manager_id)
                        }
                        this.$http.put(`asset/api/storage/${this.id}/`,this.form,{
                            headers:{
                                'token': localStorage.getItem('token')
                            }
                        }).then((res) => {
                            console.log(res)
                            this.editVisible = false
                            console.log('Response:' + JSON.stringify(res));
                            this.$message.success('修改成功');
                            this.getData()
                        }).catch( (error) =>{
                            this.$message.error(JSON.stringify(error.response.data));
                        })
                    }
                }).catch(error=>{
                    console.log(error)
                    this.$message.error("参数错误")
                    // return
                })//校验通过执行
            },
            //新增弹框
            handleAdd() {
                this.form = {};
                this.makeTitle = "增加";
                this.editVisible = true;
                this.querynetworkData = [{}]
                this.$nextTick(()=>{
                    this.$refs.form.clearValidate();
                })
            },
            // 查看网卡信息
            searchNetwork(row) {
                this.$http.get(`asset/api/network/networks/?storage_id=${row.id}`, {
                    headers: {
                        'token': localStorage.getItem('token')
                    }}).then((res) => {
                    this.querynetworkData = res.data
                    if(this.querynetworkData==""){
                        this.$message.warning('网卡数据不存在');
                    }else{
                        this.networkVisible = true
                    }
                });
            },
            //增加网卡数量
            addItem() {
                this.querynetworkData.push({
                    mac: '',
                    broadcast: '',
                    netmask: '',
                    ip: '',
                    type: ''
                })
            },
            //网卡数量减少
            del(index) {
                this.querynetworkData.splice(index, 1)
            },
            //分页
            handlePageChange(val) {
                this.$set(this.query, 'pageIndex', val);
                this.getData();
            },
            // 触发搜索按钮
            handleSearch() {
                this.$set(this.query, 'pageIndex', 1);
                this.getData();
            },
            handledelete(row) {
                this.$confirm('确定要删除吗？', '提示', {
                    type: 'warning'
                }).then(() => {this.$http.delete(`asset/api/storage/${row.id}`,  {
                    headers: {
                        'token': localStorage.getItem('token')
                    }
                }).then((res) => {
                    if (res.status === 204) {
                        this.$message.success('删除成功！');
                        this.$set(this.query, 'pageIndex', 1)
                        this.getData()
                    } else {
                        this.$message.error(res.data.msg);
                    }

                }).catch( (error)=>{
                    this.$message.error(JSON.stringify(error.response.data));
                });
                })},

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
            // 导出数据
            exportData() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["名称", "主机名", "sn", "厂商", "系列", '型号', '数据中心', '机房', '机柜', '管理ip',
                    '管理名称', '管理密码', '起始高度', '高度', '用途', '磁盘型号','磁盘容量','磁盘厂商','控制器数量','控制器系统版本',
                    '主机端口类型','主机端口数量','扩展端口类型','扩展端口数量','扩展柜类型','扩展柜数量','控制柜硬盘数量','扩展柜硬盘数量',
                    '采购时间','过保日期', '资产管理者'];// 上面设置Excel的表格第一行的标题

                    const filterVal = ["storage_name", "hostname", "sn", 'vendor', 'series', 'storage_model', 'data_center',
                    'location_zone', 'location_cabinet','manage_address', 'manage_username', 'manage_password', 'storage_start_unit',
                    'storage_unit','usage', 'disk_model','disk_capacity','disk_vendor','controller_num','controller_system_version',
                    'host_port_type','host_port_num','extension_port_type','extension_port_num','extension_rack_type','extension_rack_num',
                    'controller_rack_disk_num','extension_rack_disk_num','arrived_date','expire_date', 'asset_manager']; // 上面的index、nickName、name是tableData里对象的属性

                    this.$http.get( `asset/api/storage/?storage_name=${this.searchData.storage_name}&hostname=${this.searchData.hostname
                    }&vendor=${this.searchData.vendor}`, {
                        headers: {
                            'token': localStorage.getItem('token')
                        }}).then((res) => {
                        this.exportDataRes = res.data;
                    }).then(() =>{
                        const list = this.exportDataRes;              //把data里的tableData存到list
                        const data = this.formatJson(filterVal, list);
                        console.log(data)

                        export_json_to_excel(tHeader, data, "存储");   //标题，数据，文件名
                    })});
            },

            formatJson(filterVal, jsonData) {
                const data_list = []
                jsonData.map((v) => {
                    let filter_list = []
                    // if(v.asset_manager!=null){
                    //     v.asset_manager = v.asset_manager.username
                    // }
                    filterVal.map((j)=> {
                        if(v[j]&&j==='vendor'){
                            v[j] = v[j].vendor_name
                        }
                        if(v[j]&&j==='series'){
                            v[j] = v[j].series_name
                        }
                        if(v[j]&&j==='data_center'){
                            v[j] = v[j].dc_name
                        }
                        if(v[j]&&j==='location_zone'){
                            v[j] = v[j].room_name
                        }
                        if(v[j]&&j==='location_cabinet'){
                            v[j] = v[j].location_cabinet
                        }
                        if(v[j]&&j==='asset_manager'){
                            v[j] = v[j].username
                        }
                        filter_list.push(v[j])
                    })
                    data_list.push(filter_list)
                })
                return data_list
            },
            // 导出模版
            exportTemplate() {
                require.ensure([], () => {
                    const { export_json_to_excel } = require("../../../excel/Export2Excel");

                    const tHeader = ["名称", "主机名", "sn", '型号', '管理ip', '管理名称', '管理密码', '起始高度', '高度', '用途',
                        '磁盘型号','磁盘容量','控制器数量','控制器系统版本', '主机端口类型','主机端口数量','扩展端口类型',
                        '扩展端口数量','扩展柜类型','扩展柜数量','控制柜硬盘数量','扩展柜硬盘数量', '采购时间','过保日期'];// 上面设置Excel的表格第一行的标题

                    const list = []
                    export_json_to_excel(tHeader, list, "存储导入模版");   //标题，数据，文件名
                });
            },
            //excel上传成功时
            uploadSuccess(file){
                console.log(file);
                this.$refs.uploadExcel.clearFiles();
                this.getData()
                alert('上传成功！');
            },
            handleError(err){
                alert(err)
            },
            importExcel() {
                if(this.$refs.uploadExcel.uploadFiles.length===0){
                    this.$message.error("请选取文件")
                }else{
                    this.$refs.uploadExcel.submit();
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


</style>

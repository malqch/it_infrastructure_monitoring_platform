<template>
	<div>
		<div class="wrapper">
			<el-row :span="24" class="mlr10 mt10">
				<el-col :span="24">
					<div class="mb10">
						<el-row class="serve_select">
							<el-form ref="form" label-width="70px">

								<el-col :span="5">
									<el-form-item label="IP" label-width="50px">
										<el-select v-model="manageIp" filterable remote reserve-keyword placeholder="请输入IP" :remote-method="remoteMethod"
										class="select_width" @change="changeIp">
											<el-option v-for="(item) in optionsNetworkIp" :key="item.id" :label="item.manage_ip" :value="item.manage_ip+'/'+item.hostname">
											</el-option>
										</el-select>
									</el-form-item>
								</el-col>
								<el-col :span="12">
									<el-form-item label="起止日期">
										<el-date-picker v-model="networkTime" type="datetimerange" range-separator="至" start-placeholder="开始日期"
										end-placeholder="结束日期" class="date_width" @change="changeIp">
											>
										</el-date-picker>
									</el-form-item>
								</el-col>
							</el-form>
						</el-row>
						<el-row>
							<el-col :span="5">
								<div class="network_top_top">
									<div>
										<dl class="top_font_10 mlr10">
											<dt class="serve_name">{{storageName}}</dt>
											<dd>存储名称</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top ml10">
									<div>
										<dl class="top_font_10 mlr10 ">
											<dt class="time">{{manageIp}}</dt>
											<dd>IP</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top mlr10">
									<dl class="top_font_10">
										<dt class="serve_name">STORAGE</dt>
										<dd>网络设备类型</dd>
									</dl>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top">
									<dl class="top_font_10">
										<dt class="serve_name">{{seriesName}}</dt>
										<dd>系列名称</dd>
									</dl>
								</div>
							</el-col>
							<el-col :span="4">
								<div class="network_top_top ml10">
									<dl class="top_font_10">
										<dt class="serve_name">{{vendorName}}</dt>
										<dd>厂商</dd>
									</dl>
								</div>
							</el-col>
						</el-row>

					</div>
				</el-col>
			</el-row>

			<el-row :span="24" class="serve_center1 mlr10 mt10">
				<el-col :span="24">

					<el-tabs type="border-card" @tab-click="changeTab">
						<el-tab-pane label="节点">
							<div>
								<el-select class="change" v-model="hwperfNode" id="hwperf_node" :popper-append-to-body="false" @change="changeNode">
									<el-option v-for="item in hwperfNodeList" :key="item" :label="item" :value="item">
									</el-option>
								</el-select>
							</div>
							<el-row :span="24" :gutter="10">
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">IOPS</p>
										<div class="chartdDiv">
											<lineEcharts :id="'ipos'" :data="nodeIposData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">带宽</p>
										<div class="chartdDiv">
											<lineEcharts :id="'traffic'" :data="nodeTrafficData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">延时</p>
										<div class="chartdDiv">
											<lineEcharts :id="'delay'" :data="nodeDelayData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
							</el-row>
							
						</el-tab-pane>
						<el-tab-pane label="控制器">
							<div>
								<el-select class="change" v-model="HwinfoController" id="" :popper-append-to-body="false" @change="changeController">
									<el-option v-for="item in HwinfoControllerList" :key="item" :label="item" :value="item">
									</el-option>
								</el-select>
							</div>
							<el-row :span="24" :gutter="10">
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">CPU利用率</p>
										<div class="chartdDiv">
											<lineEcharts :id="'cpu'" :data="controllerCpuData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">内存利用率</p>
										<div class="chartdDiv">
											<lineEcharts :id="'memory'" :data="controllerMemoryData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
								<el-col :span="8">
									<div class="panel">
										<p class="title_p mt10 ml10">缓存</p>
										<div class="chartdDiv">
											<lineEcharts :id="'cache'" :data="controllerCacheData" class="ech_height"></lineEcharts>
										</div>
									</div>
								</el-col>
							</el-row>
						</el-tab-pane>
					</el-tabs>
				</el-col>

			</el-row>
			<el-row :span="24" class="mt10 ml10 mlr10">
				<el-row :span="24"  class="mt10" v-if="showController">
					<el-col :span="24">
						<el-table class="table-content" :data="tableControllerData" border max-height="200px" style="">
							<el-table-column  prop="hwStorageControllerName" label="控制器名称" align="center">
							</el-table-column>
							<el-table-column  prop="hwStorageControllerCPUInfo" label="控制器CPU信息" align="center">
							</el-table-column>
							<el-table-column  prop="hwStorageControllerVoltage" label="控制器电压" align="center">
							</el-table-column>
							<el-table-column  prop="hwStorageControllerHealthStatus" label="控制器健康状态" align="center">
								<template slot-scope="scope">
									<span  v-if="scope.row.hwStorageControllerHealthStatus==='1'">正常</span>
									<span  v-else>不正常</span>
								</template>
							</el-table-column>
							<el-table-column  prop="hwStorageControllerMemorySize" label="控制器内存" align="center">
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
				<el-row :span="24"  class="mt10" v-if="showDisk">
					<el-col :span="24">
						<el-table class="table-content" :data="tableDiskData" border max-height="200px" style="">
							<el-table-column  prop="hwInfoDiskModel" label="磁盘型号" align="center">
							</el-table-column>
							<el-table-column  prop="hwInfoDiskCapacity" label="磁盘容量" align="center">
							</el-table-column>
							<el-table-column  prop="hwInfoDiskSerialNumber" label="磁盘序列号" align="center">
							</el-table-column>
							<el-table-column  prop="hwInfoDiskType" label="磁盘类型" align="center">
								<template slot-scope="scope">
									<span  v-if="scope.row.hwInfoDiskType==='1'">SAS</span>
									<span  v-if="scope.row.hwInfoDiskType==='3'">SSD</span>
								</template>
							</el-table-column>
							<el-table-column  prop="hwInfoDiskManufacturer" label="磁盘厂商" align="center">
							</el-table-column>
							<el-table-column  prop="hwInfoDiskRunningStatus" label="运行状态" align="center">
								<template slot-scope="scope">
									<span  v-if="scope.row.hwInfoDiskRunningStatus==='27'">在线</span>
									<span  v-else>不在线</span>
								</template>
							</el-table-column>
							<el-table-column  prop="hwInfoDiskHealthStatus" label="磁盘健康状态" align="center">
								<template slot-scope="scope">
									<span  v-if="scope.row.hwInfoDiskHealthStatus==='1'">正常</span>
									<span  v-else>不正常</span>
								</template>
							</el-table-column>
							
						</el-table>
					</el-col>
				</el-row>
				<el-row :span="24" class="mt10" v-if="showLun">
					<el-col :span="24">
						<el-table class="table-content" :data="tableLunData" border max-height="200px" style="">
							<el-table-column  prop="hwInfoLunName" label="LUN名称" align="center">
							</el-table-column>
							<el-table-column  prop="hwInfoLunSubscribedCapacity" label="LUN总容量(G)" align="center">
								<template slot-scope="scope">{{scope.row.hwInfoLunSubscribedCapacity?(scope.row.hwInfoLunSubscribedCapacity/1024).toFixed(2):''}}</template>
							</el-table-column>
							<el-table-column  prop="hwInfoLunCapacity" label="LUN实际占用容量配额(G)" align="center">
								<template slot-scope="scope">{{scope.row.hwInfoLunCapacity?(scope.row.hwInfoLunCapacity/1024).toFixed(2):''}}</template>
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
			</el-row>

		</div>
	</div>
</template>
<script>
	import lineEcharts from "@/application/echart/LineStorage.vue";
	export default {
		name: 'ViewNetwork',
		components: {
			lineEcharts
		},
		data() {
			return {
				timer: null,
				networkTime: [],
				optionsNetworkIp: [],
				firmName: '',
				tableControllerData: [],
				tableDiskData: [],
				tableLunData: [],
				showController:false,
				showDisk:false,
				showLun:false,
				controllerList:[],
				diskList:[],
				lunList:[],
				nodeIposData:{
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				nodeTrafficData:{
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				nodeDelayData:{
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				storageName:'',
				manageIp:'',
				vendorName:'',
				seriesName:'',
				hwperfNode:'',
				hwperfNodeList:[],
				HwinfoController:'',
				HwinfoControllerList:[],
				controllerCpuData: {
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				controllerMemoryData:{
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				controllerCacheData:{
					lengedData: '',
					xAxisData: [],
					seriesData: [],
					animation: true
				}
			}
		},
		computed: {},
		created() {
			this.networkTime = [this.Format(new Date() - 12 * 60 * 60 * 1000), this.Format(new Date())];
		},
		mounted() {
			const url = window.document.location.href;
			const search = url.split('?');
			if (search[1] == undefined) {
				this.queryOneIp();
			} else {
				const search_ips = search[1].split('&');
				const search_ip = search_ips[0].split('=');
				this.manageIp = search_ip[1];
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.serveHistory(startTime, curTime);
			}
			this.timer = setInterval(() => {
				this.changeIp();
			}, 300000);
		},
		methods: {
			queryOneIp() {
				
				this.$http.get(`asset/api/storage/?current_page=1&pre_page=1&vendor=华为&is_monitor=是`, {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.manageIp = res.data.data[0].manage_ip;
					this.storageName = res.data.data[0].storage_name;
					this.vendorName=res.data.data[0].vendor.vendor_name;
					this.seriesName=res.data.data[0].series.series_name;
					const curTime = Date.parse(this.networkTime[1]) / 1000;
					const startTime = Date.parse(this.networkTime[0]) / 1000;
					this.serveHistory(startTime, curTime);
					
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			serveHistory(start, end) {
				this.$http.get(
				
					`monitor/api/storageitem/monitor?storage_name=STORAGE_${this.manageIp}`, {
						headers: {
							'token': localStorage.getItem('token')
						}
					}).then((res) => {
					this.hwperfNode='HWPERFNODE_1';
					this.hwperfNodeList=[];
					for(var i=1;i<=res.data.HWPERFNODEDELAY;i++){
						this.hwperfNodeList.push('HWPERFNODE_'+i)
					}
					this.getIposData(start, end,this.hwperfNode.split('_')[1]);
					this.getTrafficData(start, end,this.hwperfNode.split('_')[1]);
					this.getDelayData(start, end,this.hwperfNode.split('_')[1]);
					this.HwinfoController='HWINFOCONTROLLER_1';
					this.HwinfoControllerList=[];
					for(var j=1;j<=res.data.HWINFOCONTROLLERCPUUSAGE;j++){
						this.HwinfoControllerList.push('HWINFOCONTROLLER_'+j)
					}
					this.getCpuData(start, end,this.HwinfoController.split('_')[1]);
					this.getMemoryData(start, end,this.HwinfoController.split('_')[1]);
					this.getCacheData(start, end,this.HwinfoController.split('_')[1]);
					const resData = res.data.showTable;
					this.tableControllerData=[];
					this.tableDiskData=[];
					this.tableLunData=[];
					this.showController=false;
					this.controllerList=[];
					this.diskList=[];
					this.lunList=[];
					if(Object.prototype.hasOwnProperty.call(resData,"CONTROLLERDATALIST")){
						for(let a=0;a<resData.CONTROLLERDATALIST.length;a++){
							if(Object.prototype.hasOwnProperty.call(resData.CONTROLLERDATALIST[a],"hwStorageControllerCPUInfo")){
								this.tableControllerData.push(resData.CONTROLLERDATALIST[a])
							}
						}
						//this.tableControllerData=resData.CONTROLLERDATALIST;
						this.showController=true;
					}
					if(Object.prototype.hasOwnProperty.call(resData,"DISKLIST")){
						this.tableDiskData=resData.DISKLIST;
						this.showDisk=true;
					}
					if(Object.prototype.hasOwnProperty.call(resData,"LUNDATALIST")){
						this.tableLunData=resData.LUNDATALIST;
						this.showLun=true;
					}
					
					for(var a=0;a<resData.CONTROLLERDATALIST.length;a++){
						this.controllerList.push(resData.CONTROLLERDATALIST[a].hwStorageControllerName)
					}
					
					

				}).catch((error) => {
					console.log(error)
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getIposData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWPERFNODETOTALIOPS_`+count+`,HWPERFNODEREADIOPS_`+count+`,HWPERFNODEWRITEIOPS_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.nodeIposData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWPERFNODETOTALIOPS='HWPERFNODETOTALIOPS_'+count;
					const HWPERFNODEREADIOPS='HWPERFNODEREADIOPS_'+count;
					const HWPERFNODEWRITEIOPS='HWPERFNODEWRITEIOPS_'+count;
					this.nodeIposData.legendData = ['总', '读', '写'];
					this.nodeIposData.xAxisData = xAxis;
					this.nodeIposData.seriesData = [{
						name: "总",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#f0c725'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(204,199,37, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(204,199,37, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#f0c725',
								borderColor: '#f0c725'
							}
						},
						data: res.data[HWPERFNODETOTALIOPS]
					}, {
						name: "读",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#16f892'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(22,248,146, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(22,248,146, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#16f892',
								borderColor: '#16f892'
							}
						},
						data: res.data[HWPERFNODEREADIOPS]
					}, {
						name: "写",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#ff99e4'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(255,153,288, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(255,153,288, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#ff99e4',
								borderColor: '#ff99e4'
							}
						},
						data: res.data[HWPERFNODEWRITEIOPS]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getTrafficData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWPERFNODETOTALTRAFFIC_`+count+`,HWPERFNODEREADTRAFFIC_`+count+`,HWPERFNODEWRITETRAFFIC_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.nodeTrafficData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWPERFNODETOTALTRAFFIC='HWPERFNODETOTALTRAFFIC_'+count;
					const HWPERFNODEREADTRAFFIC='HWPERFNODEREADTRAFFIC_'+count;
					const HWPERFNODEWRITETRAFFIC='HWPERFNODEWRITETRAFFIC_'+count;
					this.nodeTrafficData.legendData = ['总', '读', '写'];
					this.nodeTrafficData.xAxisData = xAxis;
					this.nodeTrafficData.seriesData = [{
						name: "总",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#f0c725'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(204,199,37, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(204,199,37, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#f0c725',
								borderColor: '#f0c725'
							}
						},
						data: res.data[HWPERFNODETOTALTRAFFIC]
					}, {
						name: "读",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#16f892'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(22,248,146, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(22,248,146, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#16f892',
								borderColor: '#16f892'
							}
						},
						data: res.data[HWPERFNODEREADTRAFFIC]
					}, {
						name: "写",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#ff99e4'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(255,153,288, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(255,153,288, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#ff99e4',
								borderColor: '#ff99e4'
							}
						},
						data: res.data[HWPERFNODEWRITETRAFFIC]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getDelayData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWPERFNODEDELAY_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.nodeDelayData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWPERFNODEDELAY='HWPERFNODEDELAY_'+count;
					this.nodeDelayData.legendData = ['延时'];
					this.nodeDelayData.xAxisData = xAxis;
					this.nodeDelayData.seriesData = [{
						name: "延时",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#9e8cff'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(158,140,255, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(158,140,255, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#9e8cff',
								borderColor: '#9e8cff'
							}
						},
						data: res.data[HWPERFNODEDELAY]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getCpuData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWINFOCONTROLLERCPUUSAGE_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.controllerCpuData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWINFOCONTROLLERCPUUSAGE='HWINFOCONTROLLERCPUUSAGE_'+count;
					this.controllerCpuData.xAxisData = xAxis;
					this.controllerCpuData.seriesData = [{
						name: "cpu利用率",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#f0c725'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(204,199,37, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(204,199,37, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#f0c725',
								borderColor: '#f0c725'
							}
						},
						data: res.data[HWINFOCONTROLLERCPUUSAGE]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getMemoryData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWINFOCONTROLLERMEMORYUSAGE_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.controllerMemoryData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWINFOCONTROLLERMEMORYUSAGE='HWINFOCONTROLLERMEMORYUSAGE_'+count;
					this.controllerMemoryData.xAxisData = xAxis;
					this.controllerMemoryData.seriesData = [{
						name: "内存利用率",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#16f892'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(22,248,146, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(22,248,146, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#16f892',
								borderColor: '#16f892'
							}
						},
						data: res.data[HWINFOCONTROLLERMEMORYUSAGE]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			getCacheData(start, end,count) {
				this.$http.get(`monitor/api/storageitem/history?start=` + start + `&end=` + end + `&m=HWINFOCONTROLLERCACHECAPACITY_`+count+`&logic_ip=${this.manageIp}` , {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.controllerCacheData={
						lengedData: '',
						xAxisData: [],
						seriesData: [],
						animation: true
					}
					let xAxis = res.data.time.map(item => {
						return this.Format(item * 1000);
					});
					const HWINFOCONTROLLERCACHECAPACITY='HWINFOCONTROLLERCACHECAPACITY_'+count;
					this.controllerCacheData.xAxisData = xAxis;
					this.controllerCacheData.seriesData = [{
						name: "缓存",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#ff99e4'
							},
						},
						areaStyle: {
							color: {
								type: 'linear',
								x: 0,
								y: 0,
								x2: 0,
								y2: 1,
								colorStops: [{
									offset: 0,
									color: 'rgba(255,153,288, 0.8)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(255,153,288, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						itemStyle: {
							normal: {
								color: '#ff99e4',
								borderColor: '#ff99e4'
							}
						},
						data: res.data[HWINFOCONTROLLERCACHECAPACITY]
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			remoteMethod(query) {
				if (query !== '') {
					this.$http.get(`asset/api/storage/storage?vendor=华为&query=${query}&is_monitor=是`, {
						headers: {
							'token': localStorage.getItem('token')
						}
					}).then((res) => {
						this.optionsNetworkIp = [];
						this.optionsNetworkIp = res.data.map(item => {
							return item
						});
						// this.networkIp=this.optionsNetworkIp[0];
					}).catch((error) => {
						this.$message.error(JSON.stringify(error.response.data));
					});
				} else {
					this.optionsNetworkIp = [];
				}
			},
			changeTab(tab, event){
				console.log(tab)
				console.log(event)
			},
			changeIp() {
				this.manageIp = this.manageIp.split('/')[0];
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.serveHistory(startTime, curTime);
			},
			changeNode() {
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.getIposData(startTime, curTime,this.hwperfNode.split('_')[1]);
				this.getTrafficData(startTime, curTime,this.hwperfNode.split('_')[1]);
				this.getDelayData(startTime, curTime,this.hwperfNode.split('_')[1])
			},
			changeController() {
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.getCpuData(startTime, curTime,this.HwinfoController.split('_')[1]);
				this.getMemoryData(startTime, curTime,this.HwinfoController.split('_')[1]);
				this.getCacheData(startTime, curTime,this.HwinfoController.split('_')[1]);
			},
			Format(value) {
				let date = new Date(value);
				let y = date.getFullYear();
				let MM = date.getMonth() + 1;
				MM = MM < 10 ? ('0' + MM) : MM;
				let d = date.getDate();
				d = d < 10 ? ('0' + d) : d;
				let h = date.getHours();
				h = h < 10 ? ('0' + h) : h;
				let m = date.getMinutes();
				m = m < 10 ? ('0' + m) : m;
				let s = date.getSeconds();
				s = s < 10 ? ('0' + s) : s;
				return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;

			}
		},
		beforeDestroy() {
			clearInterval(this.timer);
			this.timer = null;
		}
	}
</script>
<style lang="scss" scoped>
	@import "../../../assets/css/fonts/font.css";
	@import "../../../assets/scss/echarts";
	@import "../../../assets/scss/darkStyle";

	.center {
		text-align: left;
		color: #fff;
		font-size: 14px;
	}

	.mt5 {
		margin-top: 5px;
	}

	.date_width {
		width: 335px;
	}

	.select_width {
		width: 140px;
	}

	.cpuHeight {
		height: 220px !important;
		padding: 6px 0;
	}

	.selectIp /deep/ .el-input__inner {
		color: #e5bb2e;
		font-size: 18px;
	}

	.network_top {
		border-radius: 10px;
		background: #24273e;
		height: 342px;
	}

	.network_top_top {
		border-radius: 10px;
		background: #24273e;
		height: 65px
	}

	.network_cpu {
		margin: 0 10px 10px 10px;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_top_right {
		height: 70px;
		background: #24273e;
		border-radius: 8px;
		margin-top: 10px;
	}

	.textC {
		text-align: center;
	}

	.mt16 {
		margin-top: 16px;
	}

	.serve_top_mt {
		margin: 10px 12px;
	}

	dl {
		dd {
			margin-top: 3px;
		}
	}

	.serve_center {
		padding: 10px;
		overflow: hidden;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_center1 {
		overflow: hidden;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_center,
	.serve_center1,
	.network_top {
		p {
			color: #03c2ec;
			font-size: 12px;
			padding: 10px 0 0 10px;
			font-weight: 600;
		}
	}

	.mt10 {
		margin-top: 10px;
	}

	.serve_name {
		font-size: 12px;
	}

	.serve_select {
		margin: 0 0 13px 0;
	}

	.table-content {
		border-radius: 10px;
	}

	/deep/ .el-table__body-wrapper::-webkit-scrollbar {
		width: 5px;
		height: 6px;
		background: #191b2a;
	}

	/deep/ .el-table__body-wrapper::-webkit-scrollbar-thumb {
		background-color: #596077;
		border-radius: 2px;
	}

	/deep/.el-table th {
		background-color: #2c2f49 !important;
		color: #b08ff9;
		font-weight: normal;
	}

	/deep/ .el-table--border th {
		border-right: 1px solid #2c2f49;
		border-bottom: 1px solid #2c2f49;
	}

	/deep/ .el-table td {}

	/deep/ .el-table--border td {
		border-right: 1px solid #24273e;
		border-bottom: 1px solid #24273e;
	}

	/deep/ .el-table--enable-row-hover .el-table__body tr:hover>td {
		background: #24273e !important;
	}

	/deep/ .el-table tr {
		color: #fff;
		background: #24273e;
	}

	/deep/ .el-table--border th.gutter:last-of-type {
		border-bottom: none;
	}

	/deep/ .el-table--border th {
		border-right: none;
	}

	/deep/.el-table--small td {
		padding: 2px 0;
	}

	/deep/ .el-table--small th {
		padding: 5px 0;
	}

	/deep/ .el-table .sort-caret.ascending {
		border-bottom-color: #24273e;
		top: 5px;
	}

	/deep/ .el-table .sort-caret.descending {
		border-top-color: #24273e;
		bottom: 7px;
	}

	/deep/ .el-table__empty-block {
		background: #24273e;
	}

	.panel {
		position: relative;
		/*height: 3.875rem;*/
		border: 1px solid rgba(25, 186, 139, 0.09);
		/*background: rgba(255, 255, 255, 0.04) url('../../assets/img/index/line.png');*/
		padding: 0 0.1875rem 0;

		&:before {
			position: absolute;
			top: 0;
			left: 0;
			content: "";
			width: 10px;
			height: 10px;
			border-top: 2px solid #02a6b5;
			border-left: 2px solid #02a6b5;
		}

		&:after {
			position: absolute;
			top: 0;
			right: 0;
			content: "";
			width: 10px;
			height: 10px;
			border-top: 2px solid #02a6b5;
			border-right: 2px solid #02a6b5;
		}

		.panel-footer {
			position: absolute;
			left: 0;
			bottom: 0;
			width: 100%;

			&:before {
				position: absolute;
				bottom: 0;
				left: 0;
				content: "";
				width: 10px;
				height: 10px;
				border-bottom: 2px solid #02a6b5;
				border-left: 2px solid #02a6b5;
			}

			&:after {
				position: absolute;
				bottom: 0;
				right: 0;
				content: "";
				width: 10px;
				height: 10px;
				border-bottom: 2px solid #02a6b5;
				border-right: 2px solid #02a6b5;
			}
		}

		h4 {
			height: 0.6rem;
			line-height: 0.6rem;
			text-align: center;
			color: #fff;
			font-size: 0.225rem;
			font-weight: 400;

			a {
				margin: 0 0.1875rem;
				color: #fff;
				text-decoration: none;
			}
		}

		.chart {
			height: 3rem;
		}

		ul {
			margin-left: 60px;

			li {
				color: #b3ccf8;
				font-size: 12px;
				letter-spacing: 1px;

				.warn_time_p {
					color: #a1b0cc;
					margin-top: 5px;
				}
			}

		}
	}

	.chartdDiv {
		width: 100%;
		height: 100%;
	}

	.ech_height {
		height: 220px;
		/*height:100%;*/
	}

	/deep/ .el-tabs--border-card {
		background: #24273e;
		border: none;
		color: #fff;
	}

	/deep/ .el-tabs--border-card>.el-tabs__header {
		background-color: #2c2f49;
		border-bottom: none;
	}

	/deep/ .el-tabs--border-card>.el-tabs__header .el-tabs__item {
		color: #03c2ec;
		border: none;
	}

	/deep/ .el-tabs--border-card>.el-tabs__header .el-tabs__item.is-active {
		color: #e6a23c;
		background-color: #272c4b;
		border: none;
	}

	.change {
		width: 200px;
		margin-bottom: 10px;
	}
</style>

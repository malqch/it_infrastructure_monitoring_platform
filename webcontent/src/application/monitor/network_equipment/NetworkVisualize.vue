<template>
	<div>
		<div class="wrapper">
			<el-row :span="24" class="mlr10 mt10">
				<el-col :span="18">
					<div class="mb10">
						<el-row class="serve_select">
							<el-form ref="form" label-width="70px">
								<el-col :span="3" class="ml10">
									<el-select v-model="device_type" id="device_type" :popper-append-to-body="false" @change="changeType">
										<el-option v-for="item in device_type_option" :key="item.value" :label="item.label" :value="item.value">
										</el-option>
									</el-select>
								</el-col>
								<el-col :span="7">
									<el-form-item label="IP" label-width="50px">
										<el-select v-model="networkIp" filterable remote reserve-keyword placeholder="请输入IP" :remote-method="remoteMethod"
										class="select_width" @change="changeIp">
											<el-option v-for="(item) in optionsNetworkIp" :key="item.id" :label="item.ipaddr" :value="item.ipaddr+'/'+item.name">
											</el-option>
										</el-select>
									</el-form-item>
								</el-col>
								<el-col :span="9">
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
							<el-col :span="5" v-show="isShowName">
								<div class="network_top_top">
									<div>
										<dl class="top_font_10 mlr10">
											<dt class="serve_name" style="font-size: 16px;">{{deviceName}}</dt>
											<dd>设备名称</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top ml10">
									<div>
										<dl class="top_font_10 mlr10 ">
											<dt class="time">{{IP}}</dt>
											<dd>IP</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top mlr10">
									<dl class="top_font_10">
										<dt class="serve_name">{{serviceType}}</dt>
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
						<el-row :span="24" class="mt10">
							<el-row :span="24" :gutter="10">
								<el-col :span="12">
									<el-table class="table-content" :data="tableUtilizationData" border height="200px" style="">
										<el-table-column sortable prop="name" label="网络设备" align="center">
										</el-table-column>
										<el-table-column sortable prop="value" label="1分钟利用率" align="center">
											<template slot-scope="scope">{{scope.row.value}}%</template>
										</el-table-column>
									</el-table>
								</el-col>
								<el-col :span="12">
									<el-table class="table-content" :data="tableMemoryData" border height="200px" style="">
										<el-table-column sortable prop="name" label="网络设备" align="center">
										</el-table-column>
										<el-table-column sortable prop="value" label="空闲内存" align="center">
										</el-table-column>
									</el-table>
								</el-col>
							</el-row>
						</el-row>
					</div>
				</el-col>
				<el-col :span="6">
					<div class="network_top ml10 mb10">
						<p>端口状态</p>
						<portStatus :id="'netPort'" :data="portStatusData"></portStatus>
					</div>
				</el-col>
			</el-row>

			<el-row class="serve_center">
				<el-row :span="24" class="network_cpu">
					<!-- <p>cpu历史利用率</p> -->
					<el-col :span="8" v-for="(item,index) in optionsData" :key="index" class="chart-item-area">
						<cpuUtilization :data="item" :id='"charts" +index' :index="index" class="cpuHeight"></cpuUtilization>
					</el-col>
				</el-row>
				<el-row v-show="showMore" class="btnRow">
					<el-button class="btnMore" @click="getEchartsPage">更多</el-button>
				</el-row>
			</el-row>


		</div>
	</div>
</template>
<script>
	import cpuUtilization from './visualNetworkEchart/MinutesCpuUtilization.vue';
	import portStatus from './visualNetworkEchart/portStatus.vue';

	export default {
		name: 'ViewNetwork',
		components: {
			cpuUtilization,
			portStatus
		},
		data() {
			return {
				device_type_option: [{
					value: 'SWITCH',
					label: '交换机'
				}, {
					value: 'ROUTER',
					label: '路由器'
				}],
				device_type: 'SWITCH',
				timer: null,
				chartList: [],
				optionsData: [],
				memValue: '',
				memFreeValue: '',
				networkIp: '',
				serviceType: '',
				seriesName: 0,
				vendorName: '',
				hwAvgDuty5min: '',
				hwAvgDuty1min: '',
				hwCpuDevDuty: '',
				networkTime: [],
				portStatusData: [],
				portTotal: 0,
				loading: false,
				optionsNetworkIp: [],
				ipList: [],
				loadingMore: false, //loading 加载更多
				isScroll: true, //是否可以滚动
				pageIndex: 1,
				pageSize: 10,
				list: [],
				IP: '',
				isShowName: true,
				deviceName: 'BD-2',
				tableUtilizationData: [],
				tableMemoryData: [],
				echartsPage: 1,
				showMore: false,
				ifDescR: [],
				size: 15
			}
		},
		computed: {},
		created() {
			this.networkTime = [this.Format(new Date() - 12 * 60 * 60 * 1000), this.Format(new Date())];
		},
		mounted() {
			const url = decodeURIComponent(window.document.location.href);
			//console.log('uidnlk', url);
			const search = url.split('?');
			//console.log('weiugfybckdj', search[1]);
			if (search[1] == undefined) {
				this.queryOneIp();
			} else {
				const search_ips = search[1].split('&');
				const search_ip = search_ips[0].split('=');
				const search_type = search_ips[1].split('=');
				const search_name = search_ips[2].split('=');
				this.networkIp = search_ip[1];
				const _type = search_type[1];
				if (_type == 'Switch') {
					this.device_type = 'SWITCH';
				} else if (_type == 'Router') {
					this.device_type = 'ROUTER';
				}
				//                this.isShowName=true;
				this.deviceName = search_name[1];
				
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.optionsData = [];
				this.serveHistory(startTime, curTime);
			}
			this.timer = setInterval(() => {
				this.changeIp();
			}, 300000);
		},
		methods: {
			queryOneIp() {
				let device_type_name = 'Router'
				if (this.device_type == 'SWITCH') {
					device_type_name = 'Switch'
				}
				this.$http.get(`asset/api/nro/network?type=${device_type_name}&current_page=1&pre_page=1&is_monitor=是`, {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.networkIp = res.data.data[0].ipaddr;
					this.deviceName = (res.data.data[0].hostname) ? res.data.data[0].hostname : res.data.data[0].name;
					console.log('deviceName is ......', this.deviceName);
					const curTime = Date.parse(this.networkTime[1]) / 1000;
					const startTime = Date.parse(this.networkTime[0]) / 1000;
					this.optionsData = [];
					this.serveHistory(startTime, curTime);
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data.detail));
				});
			},
			remoteMethod(query) {
				let device_type_name = 'Router'
				if (this.device_type == 'SWITCH') {
					device_type_name = 'Switch'
				}
				if (query !== '') {
					this.$http.get(`asset/api/nro/network/network?query=${query}&device_type=${device_type_name}&is_monitor=是`, {
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
						this.$message.error(JSON.stringify(error.response.data.detail));
					});
				} else {
					this.optionsNetworkIp = [];
				}
			},
			getEchartsPage() {
				this.echartsPage++;
				if (this.echartsPage * this.size >= this.portTotal) {
					this.showMore = false
				}
				console.log(this.echartsPage)
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.getEchartsData(startTime, curTime, this.size);
			},
			serveHistory(start, end) {
				console.log(this.deviceName)
				this.$http.get(
					`monitor/api/network_monitor/monitor/?network_name=${this.device_type}_${this.networkIp}_${this.deviceName}`, {
						headers: {
							'token': this.token,
							// 'responseType':'arraybuffer',
							// 'Content-Type':'application/json;charset=UTF-8',
							// 'Accept':'application/json;charset=UTF-8'
						}
					}).then((res) => {
					const resData = res.data;
					this.IP = resData.SYSUPTIME.ip;
					this.serviceType = resData.SYSUPTIME.serviceType;
					this.seriesName = resData.SYSUPTIME.seriesName;
					this.vendorName = resData.SYSUPTIME.vendorName;
					
					this.tableUtilizationData=[];
					this.tableMemoryData=[];
					this.portStatusData=[];

					for (let item in resData.HWAVGDUTY1MIN) {
						this.tableUtilizationData.push({
							name: item,
							value: resData.HWAVGDUTY1MIN[item]
						})
					}

					for (let item in resData.HWENTITYMEMUSAGE) {
						this.tableMemoryData.push({
							name: item,
							value: resData.HWENTITYMEMUSAGE[item]
						})
					}

					// const portStatusArr = [];

					for (let item in resData.PORT_STATUS) {
						this.portStatusData.push({
							name: item.substring(14),
							value: resData.PORT_STATUS[item]
						})
					}
					// this.portStatusData = portStatusArr;
					this.portTotal = resData.IFDESCR.length;
					this.ifDescR = resData.IFDESCR;
					if (resData.IFDESCR.length <= this.size) {
						this.getEchartsData(start, end, resData.IFDESCR.length);
					} else {
						this.getEchartsData(start, end, this.size);
						this.showMore = true;
					}

				}).catch((error) => {
					console.log(error)
					this.$message.error(JSON.stringify(error.response.data.detail));
				});
			},
			getEchartsData(start, end, size) {

				for (let i = (this.echartsPage - 1) * size; i < this.echartsPage * size; i++) {
					let chartListObj = {};
					chartListObj.title = this.ifDescR[i];
					chartListObj.legendData = ['入口流量', '出口流量', '入口丢包率', '出口丢包率'];
					const ifOutOctets = 'IFOUTOCTETS_' + this.ifDescR[i];
					const ifInOctets = 'IFINOCTETS_' + this.ifDescR[i];
					const ifInDiscards = 'IFINDISCARDS_' + this.ifDescR[i];
					const ifOutDiscards = 'IFOUTDISCARDS_' + this.ifDescR[i];
					this.$http.get(`monitor/api/network_monitor/history/?start=` + start + `&end=` + end + `&m=` + ifOutOctets +
						`,` + ifInOctets + `,` + ifInDiscards + `,` + ifOutDiscards + `&logic_ip=` + this.networkIp, {
							headers: {
								'token': this.token
							}
						}).then((res) => {
						if (Object.prototype.hasOwnProperty.call(res.data, 'time')) {
							const chartsTime = res.data.time;
							let xAxis = chartsTime.map(item => {
								return this.Format(item * 1000);
							});
							chartListObj.xAxisData = xAxis;

							chartListObj.seriesData = [{
								name: "入口流量",
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
								data: res.data[ifInOctets]
							}, {
								name: "出口流量",
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
								data: res.data[ifOutOctets]
							}, {
								name: "入口丢包率",
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
								data: res.data[ifInDiscards]
							}, {
								name: "出口丢包率",
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
								data: res.data[ifOutDiscards]
							}];
							this.optionsData.push(chartListObj);
							this.optionsData.sort(function(a, b) {
								let port_num_a = a.title.split('_');
								let port_num_b = b.title.split('_');
								return port_num_a[1] - port_num_b[1];
							});
						}
					}).catch((error) => {
						this.$message.error(JSON.stringify(error.response.data.detail));
					});
				}
			},
			changeIp() {
				if(this.networkIp.split('/').length==2){
					this.deviceName = this.networkIp.split('/')[1];
				}
				
				console.log('deviceName11 is ......', this.deviceName);
				this.networkIp = this.networkIp.split('/')[0];
				this.optionsData = [];
				this.showMore = false;
				const curTime = Date.parse(this.networkTime[1]) / 1000;
				const startTime = Date.parse(this.networkTime[0]) / 1000;
				this.serveHistory(startTime, curTime);
			},
			changeType() {
				this.networkIp = '';
				this.deviceName = '';
				this.optionsNetworkIp=[];
				this.queryOneIp();
				this.optionsData = [];
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
		width: 145px;
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

	.serve_center,
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
		font-size: 14px!important;
		
	}
	.time{
		font-size: 20px!important;
	}
	.top_font_10{
		line-height: 16px!important;
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
		padding: 0;
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

	.btnMore {
		background: none;
		border: 1px solid #fff;
		color: #fff;
		width: 150px;
		margin: 0 auto;
	}

	.btnRow {
		display: flex;
	}
</style>

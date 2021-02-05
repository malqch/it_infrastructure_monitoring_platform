<template>
	<div>
		<div class="wrapper">
			<el-row class="serve_select">
				<el-form ref="form" label-width="100px">
					<el-col :span="9">
						<el-form-item label="Websphere">
							<el-select v-model="weblogicHost" filterable remote reserve-keyword placeholder="请输入服务器名称或IP" :remote-method="queryWeblogic"
							class="selectIp" @change="changeQueryHost">
								<el-option v-for="(item) in weblogicData" :key=item.id :label="`${item.port}/${item.ip_address}`" :value="`${item.port}/${item.ip_address}`">
								</el-option>
							</el-select>
						</el-form-item>
					</el-col>
					<el-col :span="15">
						<el-form-item label="起止日期">
							<el-date-picker v-model="monitorTime" type="datetimerange" range-separator="至" start-placeholder="开始日期"
							end-placeholder="结束日期" class="mt16" @change="changeQueryHost">
							</el-date-picker>
						</el-form-item>
					</el-col>
				</el-form>
			</el-row>
			<el-row class="weblogic_top" :gutter="10">
				<el-col :span="5">
					<el-row class="web_top_top">
						<dl class="top_font_m18">
							<dt class="weblogic_name">{{vm_name}}</dt>
							<dd>名称</dd>
						</dl>
					</el-row>
					<el-row class="web_top_cent mtb10">
						<dl class="top_font_m18">
							<dt class="time">{{startTime}}</dt>
							<dd>开启时间</dd>
						</dl>
					</el-row>
					<el-row class="web_top_bot">
						<dl class="top_font_m18">
							<dt class="time">{{ContinuousWorkingHours}}</dt>
							<dd>连续工作时间</dd>
						</dl>
					</el-row>
				</el-col>
				<el-col :span="19">
					<el-row class="weblogic_t_top" :gutter="10">
						<el-col :span="4" style="padding-left: 0;">
							<div class="web_t">
								<dl class="top_font_web">
									<dt class="time">{{weblogicIp}}</dt>
									<dd>IP</dd>
								</dl>
							</div>
						</el-col>
						<el-col :span="3">
							<div class="web_t">
								<dl class="top_font_web">
									<dt class="weblogic_name">{{weblogicName}}</dt>
									<dd>端口</dd>
								</dl>
							</div>
						</el-col>
						<el-col :span="17" style="padding-right: 0;">
							<div class="web_t web_t_r">
								<el-col :span="6">
									<weblogicswapprec :id="swapUse" :data="SwapData"></weblogicswapprec>
								</el-col>
								<el-col :span="6">
									<memUtilization :id="memUse" :data="memData"></memUtilization>
								</el-col>
								<el-col :span="6">
									<weblogicheapprec :id="heapUse" :data="heapData"></weblogicheapprec>
								</el-col>
								<el-col :span="6">
									<weblogicnonheapprec :id="nonheapUse" :data="NonHeap"></weblogicnonheapprec>
								</el-col>
							</div>

						</el-col>
					</el-row>
					<el-row class="weblogic_bottom m10 ml10 mr10" :gutter="10">
						<el-col :span="12">
							<div class="weblogic_bot">
								<p>cpu详细信息</p>
								<WeblogicCpukList :id="cpuList" :data="cpuListData"></WeblogicCpukList>
							</div>
						</el-col>
						<el-col :span="12">
							<div class="weblogic_bot">
								<p>线程池</p>
								<WeblogickFileList :id="fileList" :data="fileListData"></WeblogickFileList>
							</div>
						</el-col>
					</el-row>
				</el-col>
			</el-row>
			<el-row class="weblogic_bottom mlr10 m10 " :gutter="10">
				<el-col :span="12">
					<div class="weblogic_bot">
						<p>内存详细信息</p>
						<WeblogicMemList :id="memList" :data="memListData"></WeblogicMemList>
					</div>
				</el-col>
				<el-col :span="12">
					<div class="weblogic_bot">
						<p>线程详细信息</p>
						<WeblogicThreadList :id="threadList" :data="threadListData"></WeblogicThreadList>
					</div>
				</el-col>
			</el-row>
			<el-row class="serve_center m10 mlr10" :gutter="10">
				<el-col :span="12">
					<div class="serve_center_left">
						<p>系统cpu利用率</p>
						<linegraph :id="'bargraphSysCpuLoad'" :data="optionSysCpuLoad" class="linegraph"></linegraph>
					</div>
				</el-col>
				<el-col :span="12">
					<div class="serve_center_left">
						<p>系统cpu平均负载</p>
						<linegraph :id="'bargraphSysCpuLoadAvg'" :data="optionSysCpuLoadAvg" class="linegraph"></linegraph>
					</div>
				</el-col>
			</el-row>
		</div>
	</div>
</template>
<script>
	import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
	import weblogicswapprec from "./weblogicEchart/WeblogicSwapPrec";
	import memUtilization from './weblogicEchart/WeblogicMemPrec';
	import weblogicheapprec from './weblogicEchart/WeblogicHeapPrec';
	import weblogicnonheapprec from './weblogicEchart/WeblogicNonHeapPrec';
	import WeblogicMemList from './weblogicEchart/WeblogicMemList';
	import WeblogicCpukList from './weblogicEchart/WeblogicCpukList';
	import WeblogicThreadList from './weblogicEchart/WeblogicThreadList';
	import WeblogickFileList from './weblogicEchart/WeblogickFileList';
	import {
		timestampToTime
	} from '../../../util/formatData';

	export default {
		name: "WeblogicMiddleware",
		components: {
			weblogicswapprec,
			memUtilization,
			weblogicheapprec,
			weblogicnonheapprec,
			WeblogicMemList,
			WeblogicCpukList,
			WeblogickFileList,
			WeblogicThreadList,
			linegraph
		},
		data() {
			return {
				swapUse: 'swapUse',
				SwapData: null,
				memUse: 'memUse',
				memData: null,
				heapUse: 'heapUse',
				heapData: null,
				nonheapUse: 'nonheapUse',
				NonHeap: 0,
				memList: '',
				memListData: [],
				AvailableProcessors: '',
				cpuList: '',
				cpuListData: [],
				threadList: '',
				threadListData: [],
				fileList: '',
				fileListData: [],

				weblogicName: '',
				weblogicIp: '10.10.10.130',
				vm_version: '',
				version: '',
				vm_vendor: '',
				startTime: '',
				vm_name: '',
				ContinuousWorkingHours: "",

				optionSysCpuLoad: {
					title: '',
					legendData: [],
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				optionSysCpuLoadAvg: {
					title: '',
					legendData: [],
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				monitorTime: '',
				weblogicData: null,
				weblogicHost: '',
			}
		},
		computed: {},
		created() {
			this.monitorTime = [this.Format(new Date() - 12 * 60 * 60 * 1000), this.Format(new Date())];
			this.queryOneWeblogic();
			this.timer = setInterval(() => {
				this.changeQueryHost();
			}, 180000);
		},
		mounted() {},
		methods: {
			queryOneWeblogic() {
				this.$http.get(`monitor/api/middleware/?middleware_type=WEBSPHERE&current_page=1&pre_page=1&is_monitor=是`, {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					const oneWeblogicData = res.data;
					const ip = oneWeblogicData.data[0].ip_address;
					const port = oneWeblogicData.data[0].port;
					this.weblogicHost = port + '/' + ip;
					this.optionData(ip, port);
					const curTime = Date.parse(this.monitorTime[1]) / 1000;
					const startTime = Date.parse(this.monitorTime[0]) / 1000;
					this.serveHistory(startTime, curTime, ip);
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			queryWeblogic(query) {
				if (query !== '') {
					this.$http.get(`monitor/api/middleware/search?middleware_type=WEBSPHERE&query=${query}&is_monitor=是`, {
						headers: {
							'token': localStorage.getItem('token')
						}
					}).then((res) => {
						this.weblogicData = res.data;
					}).catch((error) => {
						this.$message.error(JSON.stringify(error.response.data));
					});
				} else {
					this.optionsNetworkIp = [];
				}
			},
			changeQueryHost() {
				const curTime = Date.parse(this.monitorTime[1]) / 1000;
				const startTime = Date.parse(this.monitorTime[0]) / 1000;
				const weblogic_name = this.redisHost.split('/');
				const weblogic_port = weblogic_name[0];
				const weblogic_ip = weblogic_name[1];
				this.optionData(weblogic_ip, weblogic_port);
				this.serveHistory(startTime, curTime, weblogic_ip);
			},
			optionData(weblogic_ip, weblogic_port) {
				this.$http.get(`monitor/api/middleware/monitor/?middleware_name=WEBSPHERE_${weblogic_ip}_${weblogic_port}`, {
					headers: {
						'token': this.token
					}
				}).then((res) => {
					this.weblogicName = res.data.INSTALL_NAME;
					this.weblogicIp = res.data.LOGIC_IP;
					this.startTime = res.data.STARTTIME;
					this.vm_version = res.data.VMVERSION;
					this.version = res.data.VERSION;
					this.vm_vendor = res.data.VMVENDOR;
					this.vm_name = res.data.VMNAME;
					this.AvailableProcessors = res.data.AVAILABLEPROCESSORS;
					this.ContinuousWorkingHours = res.data.CONTINUOUSWORKINGHOURS;
					this.SwapData = Math.round(((res.data.TOTALSWAPSPACESIZE - res.data.FREESWAPSPACESIZE) / res.data.TOTALSWAPSPACESIZE) *
						100) / 100;
					this.memData = Math.round((res.data.FREEPHYSICALMEMORYSIZE / res.data.TOTALPHYSICALMEMORY) * 100) / 100;
					this.heapData = Math.round(Number(res.data.HEAP.split('%')[0])) / 100;
					this.NonHeap = Math.round(Number(res.data.NONHEAP.split('%')[0])) / 100;
					const FreePhysicalMemorySize = parseFloat(res.data.FREEPHYSICALMEMORYSIZE / 1024 / 1024 / 1024).toFixed(2)
					const TotalPhysicalMemorySize = parseFloat(res.data.TOTALPHYSICALMEMORY / 1024 / 1024 / 1024).toFixed(2)
					const TotalSwapSpaceSize = parseFloat(res.data.TOTALSWAPSPACESIZE / 1024 / 2014 / 1024).toFixed(2)
					const FreeSwapSpaceSize = parseFloat(res.data.FREESWAPSPACESIZE / 1024 / 2014 / 1024).toFixed(2)
					this.memListData = [{
						FreePhysicalMemorySize: FreePhysicalMemorySize,
						TotalPhysicalMemorySize: TotalPhysicalMemorySize,
						TotalSwapSpaceSize: TotalSwapSpaceSize,
						FreeSwapSpaceSize: FreeSwapSpaceSize
					}]
					//                    this.cpuListData = [{SystemCpuLoad: parseFloat(res.data.SystemCpuLoad*100).toFixed(2)+'%',
					this.cpuListData = [{
						SystemCpuLoad: parseFloat(res.data.SYSTEMCPULOAD * 100).toFixed(2) + '%',
						ProcessCpuLoad: parseFloat(res.data.PROCESSCPULOAD * 100).toFixed(2) + '%',
						SystemLoadAverage: parseFloat(res.data.SYSTEMLOADAVERAGE * 100).toFixed(2) + '%',
						// ProcessCpuTime: res.data.ProcessCpuTime,
						ProcessCpuTime: timestampToTime(res.data.PROCESSCPUTIME / 1000),
						AvailableProcessors: res.data.AVAILABLEPROCESSORS
					}]
					this.threadListData = [{
						DaemonThreadCount: res.data.DAEMONTHREADCOUNT,
						PeakThreadCount: res.data.PEAKTHREADCOUNT,
						TotalStartedThreadCount: res.data.TOTALSTARTEDTHREADCOUNT,
						ThreadCount: res.data.THREADCOUNT
					}]
					this.fileListData = [{
						JVMTHREADGROUPNAMES: res.data.JVMTHREADGROUPNAMES,
						THREADPOOLRENEWALDELAYFACTOR: res.data.THREADPOOLRENEWALDELAYFACTOR,
						LEAKSWEEPERDELAY: res.data.LEAKSWEEPERDELAY
					}]
					console.log(this.fileListData);

				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},

			serveHistory(startTime, curTime, ip) {
				this.$http.get(`monitor/api/middleware/history/?start=` + startTime + `&end=` + curTime +
					`&m=sum:SYSTEMCPULOAD{logicIp=${ip}}`, {
						headers: {
							'token': this.token
						}
					}).then((res) => {
					const lineTime = Object.keys(res.data);
					const lineXtime = [];
					for (let item in lineTime) {
						lineXtime.push(this.Format(lineTime[item] * 1000));
					}
					const linevla = Object.values(res.data);
					this.optionSysCpuLoad.xAxisData = lineXtime;
					this.optionSysCpuLoad.seriesData = [{
						name: "系统cpu利用率",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#a86ad1'
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
									color: 'rgba(168,106,209, 0.9)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(168,106,209, 0)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						color: "#fff",
						data: linevla
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});

				this.$http.get(`monitor/api/middleware/history/?start=` + startTime + `&end=` + curTime +
					`&m=sum:SYSTEMLOADAVERAGE{logicIp=${ip}}`, {
						headers: {
							'token': this.token
						}
					}).then((res) => {
					const lineTime = Object.keys(res.data);
					const lineXtime = [];
					for (let item in lineTime) {
						lineXtime.push(this.Format(lineTime[item] * 1000));
					}
					const linevla = Object.values(res.data);
					this.optionSysCpuLoadAvg.xAxisData = lineXtime;
					this.optionSysCpuLoadAvg.seriesData = [{
						name: "系统cpu平均负载",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#d1471c'
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
									color: 'rgba(209,71,28, 0.9)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(209,71,28, 0.1)' // 100% 处的颜色
								}],
								global: false // 缺省为 false
							},
							shadowColor: 'rgba(0, 0, 0, 0.1)',
							shadowBlur: 10
						},
						color: "#fff",
						data: linevla
					}];
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
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
				return y + '-' + MM + '-' + d + ' ' + h + ':' + m;

			},
		},
		beforeDestroy() {
			clearInterval(this.timer);
		}
	}
</script>
<style lang="scss" scoped>
	@import "../../../assets/css/fonts/font.css";
	@import "../../../assets/scss/echarts";

	.linegraph {
		height: 170px;
	}

	.weblogic_top {
		border-radius: 10px;
		margin: 10px 10px !important;
		height: 280px;
	}

	.web_top_top,
	.web_top_cent,
	.web_top_bot {
		height: 85px;
		border-radius: 10px;
		background: #24273e;
	}

	.top_font_m18 {
		text-align: center;
		margin-top: 18px;
	}

	.weblogic_t_top {
		margin: 0px !important;
	}

	.weblogic_t_bot {
		height: 145px;
		background: #24273e;
		border-radius: 10px;
	}

	.web_t_left,
	.web_t_cen,
	.web_t_rig {
		height: 120px;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_center_left {
		height: 220px;
		background: #24273e;
		border-radius: 10px;
	}

	.web_t_cen,
	.web_t_rig {
		// margin-left:13px;
	}

	.top_font_web {
		text-align: center;
		padding-top: 38px;
	}

	.weblogic_bot_left,
	.weblogic_bot_right,
	.weblogic_bot_center {
		height: 145px !important;
		background: #24273e;
		border-radius: 10px;
	}

	.weblogic_bot_left {
		// margin:0 10px 0px 15px;
	}

	.weblogic_bot {
		background: #24273e;
		height: 145px;
		border-radius: 10px;
		padding: 0;
	}

	dl {

		dd {
			margin-top: 5px;
		}
	}

	p {
		color: #03c2ec;
		font-size: 12px;
		padding: 10px 0 0 10px;
		font-weight: 600;
	}

	.weblogic_name {
		font-size: 14px;
	}

	/deep/ .el-col {
		margin: 0 !important;
	}

	.web_t {
		height: 120px;
		background: #24273e;
		border-radius: 10px;
		clear: both;
	}

	.mlr10 {
		margin-left: 10px !important;
		margin-right: 10px !important;
		;
	}

	.m10 {
		margin-bottom: 10px !important;
	}

	.web_t_r {
		padding-right: 0 !important;
	}
</style>

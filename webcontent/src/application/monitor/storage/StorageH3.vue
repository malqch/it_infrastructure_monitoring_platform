<template>
	<div>
		<div class="wrapper">
			<el-row :span="24" class="mlr10 mt10">
				<el-col :span="24">
					<div class="">
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
							</el-form>
						</el-row>
						<el-row class="mt10">
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
						<el-row class="mt10">
							<el-col :span="5">
								<div class="network_top_top">
									<div>
										<dl class="top_font_10 mlr10">
											<dt class="serve_name">{{serialNumber}}</dt>
											<dd>序列号</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top ml10">
									<div>
										<dl class="top_font_10 mlr10 ">
											<dt class="serve_name">{{totalCapacityMiB?(totalCapacityMiB/1024).toFixed(2):''}}</dt>
											<dd>总容量(GB)</dd>
										</dl>
									</div>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top mlr10">
									<dl class="top_font_10">
										<dt class="serve_name">{{freeCapacityMiB?(freeCapacityMiB/1024).toFixed(2):''}}</dt>
										<dd>空闲容量(GB)</dd>
									</dl>
								</div>
							</el-col>
							<el-col :span="5">
								<div class="network_top_top">
									<dl class="top_font_10">
										<dt class="serve_name">{{totalNodes}}</dt>
										<dd>节点</dd>
									</dl>
								</div>
							</el-col>
							<el-col :span="4">
								<div class="network_top_top ml10">
									<dl class="top_font_10">
										<dt class="serve_name">{{masterNode}}</dt>
										<dd>主节点</dd>
									</dl>
								</div>
							</el-col>
						</el-row>
					</div>
				</el-col>
			</el-row>


			<el-row :span="24" class="mt10 ml10 mlr10">
				<el-row :span="24" class="mt10">
					<el-col :span="24" class="table-content-box">
						<p>主机</p>
						<el-table class="table-content" :data="tableHostsData" border height="200px" style="">
							<el-table-column prop="name" label="名称" align="center">
							</el-table-column>
							<el-table-column prop="os" label="系统" align="center">
							</el-table-column>
							<el-table-column prop="FCPaths" label="FCPaths" align="center">
								<template slot-scope="scope">
									<el-button type="text" @click="handleFCPaths(scope.$index, scope.row)">
										详情
									</el-button>
								</template>
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
				<el-row :span="24" class="mt10">
					<el-col :span="24" class="table-content-box">
						<p>端口</p>
						<el-table class="table-content" :data="tablePortsData" border height="200px" style="">

							<el-table-column prop="portWWN" label="WWN端口名称" align="center">
							</el-table-column>
							<el-table-column prop="nodeWWN" label="WWN节点名称" align="center">
							</el-table-column>
							<el-table-column prop="linkState" label="连接状态" align="center">
								<template slot-scope="scope">
									<span v-if="scope.row.linkState==1">配置等待</span>
									<span v-else-if="scope.row.linkState==3">登录等待</span>
									<span v-else-if="scope.row.linkState==4">已连接</span>
									<span v-else-if="scope.row.linkState==5">连接失败</span>
									<span v-else-if="scope.row.linkState==10">离线</span>
									<span v-else>连接异常</span>
								</template>
							</el-table-column>
							<el-table-column prop="type" label="类型" align="center">
								<template slot-scope="scope">
									<span v-if="scope.row.type==1">FC端口已连接到主机</span>
									<span v-else-if="scope.row.type==2">FC端口已连接到磁盘</span>
									<span v-else-if="scope.row.type==3">端口未连接</span>
									<span v-else-if="scope.row.type==4">iport输入模式</span>
									<span v-else>未知状态</span>
								</template>
							</el-table-column>
							<el-table-column prop="mode" label="mode" align="center">
								<template slot-scope="scope">
									<span v-if="scope.row.mode==1">目标端口初始化</span>
									<span v-else-if="scope.row.mode==2">目标端口已连接</span>
									<span v-else-if="scope.row.mode==3">启动器端口已连接到磁盘</span>
									<span v-else-if="scope.row.mode==4">远程以太网复制端口</span>
								</template>
							</el-table-column>
							<el-table-column prop="device" label="设备信息" align="center" :show-overflow-tooltip="false">
								<template slot-scope="scope">
									<el-tooltip class="item" effect="dark" placement="top">
										<div v-html="scope.row.device" slot="content"></div>
										<div class="lineCls">{{changeBr(scope.row.device)}}</div>
									</el-tooltip>
								</template>
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
				<el-row :span="24" class="mt10">
					<el-col :span="24" class="table-content-box">
						<p>VLUN</p>
						<el-table class="table-content" :data="tableLunsData" border height="200px" style="">
							<el-table-column prop="volumeName" label="名称" align="center">
							</el-table-column>
							<el-table-column prop="hostname" label="主机名" align="center">
							</el-table-column>
							<el-table-column prop="active" label="状态" align="center">
								<template slot-scope="scope">{{scope.row.active==true?'活跃VLUN':'VLUN模板'}}</template>
							</el-table-column>
							<el-table-column prop="type" label="类型" align="center">
								<template slot-scope="scope">
									<span v-if="scope.row.type==1">空</span>
									<span v-else-if="scope.row.type==2">端口</span>
									<span v-else-if="scope.row.type==3">主机</span>
									<span v-else-if="scope.row.type==4">匹配设置</span>
									<span v-else-if="scope.row.type==5">主机设置</span>
								</template>
							</el-table-column>
							<el-table-column prop="remoteName" label="远端主机名" align="center">
							</el-table-column>
							<el-table-column prop="portPos" label="位置信息(节点_槽位_板卡号)" align="center">
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
				<el-row :span="24" class="mt10">
					<el-col :span="24" class="table-content-box">
						<p>VOLUME</p>
						<el-table class="table-content" :data="tableVolumesData" border height="200px" style="">
							<el-table-column prop="name" label="名称" align="center">
							</el-table-column>
							<el-table-column prop="sizeMiB" label="内存(GB)" align="center">
								<template slot-scope="scope">{{(scope.row.sizeMiB/1024).toFixed(2)}}</template>
							</el-table-column>
							<el-table-column prop="usedMiB" label="使用内存(GB)" align="center">
								<template slot-scope="scope">{{(scope.row.usedMiB/1024).toFixed(2)}}</template>
							</el-table-column>
							<el-table-column prop="freeMiB" label="空闲内存(GB)" align="center">
								<template slot-scope="scope">{{(scope.row.freeMiB/1024).toFixed(2)}}</template>
							</el-table-column>
							<el-table-column prop="state" label="状态" align="center">
								<template slot-scope="scope">{{scope.row.state==1?'正常':'不正常'}}</template>
							</el-table-column>
							<el-table-column prop="copyType" label="copyType" align="center">
								<template slot-scope="scope">
									<span v-if="scope.row.copyType==1">不复制</span>
									<span v-else-if="scope.row.copyType==2">全部复制</span>
									<span v-else-if="scope.row.copyType==3">快照复制</span>
								</template>
							</el-table-column>
							<el-table-column prop="readOnly" label="只读" align="center">
								<template slot-scope="scope">{{scope.row.readOnly==false?'否':'是'}}</template>
							</el-table-column>
						</el-table>
					</el-col>
				</el-row>
			</el-row>
			<el-dialog title="FCPaths" :visible.sync="FCPathsVisible" width="50%">
				<el-table class="table-content" :data="FCPathsData" border max-height="200px" style="">
					<el-table-column prop="wwn" label="wwn名称" align="center">
					</el-table-column>
					<el-table-column prop="portPos" label="位置信息(节点_槽位_板卡号)" align="center">
					</el-table-column>
				</el-table>
				<!-- <span slot="footer" class="dialog-footer">
					<el-button @click="editVisible = false" class="change_el_button">取 消</el-button>
					<el-button type="primary" @click="editVisible = false">确 定</el-button>
				</span> -->
			</el-dialog>
		</div>
	</div>
</template>
<script>
	export default {
		name: 'ViewNetwork',
		components: {
		},
		data() {
			return {
				timer: null,
				optionsNetworkIp: [],
				storageName: '',
				manageIp: '',
				vendorName: '',
				seriesName: '',
				totalNodes: '',
				masterNode: '',
				serialNumber: '',
				totalCapacityMiB: '',
				freeCapacityMiB: '',
				tableHostsData: [],
				tablePortsData: [],
				tableVolumesData: [],
				tableLunsData: [],
				FCPathsVisible: false,
				FCPathsData: []
			}
		},
		computed: {},
		created() {
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
				this.serveHistory();
			}
			this.timer = setInterval(() => {
				this.changeIp();
			}, 300000);
		},
		methods: {
			changeBr(val) {
				if (val) {
					return (val.toString()).replace(/<br\/>/g, '\n')
				}

			},
			queryOneIp() {

				this.$http.get(`asset/api/storage/?current_page=1&pre_page=1&vendor=华三&is_monitor=是`, {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					this.manageIp = res.data.data[0].manage_ip;
					this.storageName = res.data.data[0].storage_name;
					this.vendorName = res.data.data[0].vendor.vendor_name;
					this.seriesName = res.data.data[0].series.series_name;

					this.serveHistory();

				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			serveHistory() {
				this.$http.get(

					`monitor/api/storageitem/monitor?storage_name=STORAGE_${this.manageIp}`, {
						headers: {
							'token': localStorage.getItem('token')
						}
					}).then((res) => {
					//console.log(res)
					this.totalNodes = '';
					this.serialNumber = '';
					this.masterNode = '';
					this.totalCapacityMiB = '';
					this.freeCapacityMiB = '';
					this.tableHostsData = [];
					this.tablePortsData = [];
					this.tableVolumesData = [];
					this.tableLunsData = [];
					this.totalNodes = res.data.SYSTEM.totalNodes;
					this.serialNumber = res.data.SYSTEM.serialNumber;
					this.masterNode = res.data.SYSTEM.masterNode;
					this.totalCapacityMiB = res.data.SYSTEM.totalCapacityMiB;
					this.freeCapacityMiB = res.data.SYSTEM.freeCapacityMiB;
					this.tableHostsData = res.data.HOSTS;
					this.tablePortsData = res.data.PORTS;
					this.tableVolumesData = res.data.VOLUMES;
					this.tableLunsData = res.data.VLUNS;

				}).catch((error) => {
					//console.log(error)
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			handleFCPaths(index, row) {
				this.FCPathsVisible = true;
				this.FCPathsData = row.FCPaths
			},
			remoteMethod(query) {
				if (query !== '') {
					this.$http.get(`asset/api/storage/storage?vendor=华三&query=${query}&is_monitor=是`, {
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
			changeIp() {
				this.manageIp = this.manageIp.split('/')[0];
				this.serveHistory();
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
		width: 125px;
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

	.table-content-box {
		border-radius: 10px;
		background: #24273e;
		color: #fff;
		overflow: hidden;
		padding-bottom: 10px;
	}

	.table-content-box p {
		line-height: 35px;
		padding-left: 20px;
		color: #03c2ec;
		font-size: 14px;
		font-weight: bold;
	}

	.table-content {
		// border-radius: 10px;

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

	.lineCls {
		overflow: hidden;
		white-space: nowrap;
		text-overflow: ellipsis;
	}

	/deep/ .el-dialog__title {
		color: #fff;
	}

	/deep/ .el-dialog__body {
		padding-top: 0;
	}

	/deep/ .el-dialog__body .el-table {
		background: #151827;
	}

	/deep/ .el-dialog__body .el-table tr {
		background: #151827;
	}

	/deep/ .el-dialog__body .el-table td {
		border: none;
	}
</style>

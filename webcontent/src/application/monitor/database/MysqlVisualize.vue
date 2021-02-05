<template>
	<div>
		<div class="wrapper">
			<el-row class="serve_select">
				<el-form ref="form" label-width="100px">
					<el-col :span="9">
						<el-form-item label="mysql">
							<el-select v-model="mysqlDatabase" filterable remote reserve-keyword placeholder="请输入服务器名称或IP" :remote-method="queryMysqlDB"
							class="selectIp" @change="changeQueryHost">
								<el-option v-for="(item) in mysqlData" :key=item.id :label="`${item.sid}/${item.ip_address}`" :value="`${item.sid}/${item.ip_address}`">
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
			<el-row class="serve_top m10">
				<el-col :span="6">
					<div class="serve_top_char">
						<dl class="top_font_10">
							<dt class="time">{{serveIp}}</dt>
							<dd>服务器IP</dd>
						</dl>
					</div>
					<div class="serve_top_char mtb10">
						<dl class="top_font_10">
							<dt class="time">{{port}}</dt>
							<dd>端口</dd>
						</dl>
					</div>
					<div class="serve_top_char">
						<dl class="top_font_10">
							<dt class="serve_name">{{version_comment}}</dt>
							<dd>version_comment</dd>
						</dl>
					</div>
					<div class="serve_top_char mtb10">
						<dl class="top_font_10">
							<dt class="time">{{version}}</dt>
							<dd>版本</dd>
						</dl>
					</div>
					<div class="serve_top_char">
						<dl class="top_font_10">
							<dt class="time">{{uptime}}天</dt>
							<dd>运行时间</dd>
						</dl>
					</div>
				</el-col>
				<el-col :span="9">
					<div class="serve_bottom_left mlr10">
						<p>SQL执行信息</p>
						<el-table class="table-content" :data="sql_avg_time_table_data" border height="361px" style="">
							<el-table-column prop="schema_name" label="SCHEMA名称" align="center">
							</el-table-column>
							<el-table-column prop="count" label="执行数量" align="center">
							</el-table-column>
							<el-table-column prop="err_count" label="错误数量" align="center">
							</el-table-column>
							<el-table-column prop="avg_microsec" label="平均执行时间" align="center">
							</el-table-column>
						</el-table>
						<!-- <SqlAvgTime :id="sql_avg_time_table" :data="sql_avg_time_table_data"></SqlAvgTime> -->
					</div>
				</el-col>
				<el-col :span="9">
					<div class="serve_bottom_left">
						<p>索引文件</p>
						<el-table class="table-content" :data="sql_disk_usage_table_data" border height="361px" style="">
							<el-table-column prop="TABLE_SCHEMA" label="SCHEMA名称" align="center">
							</el-table-column>
							<el-table-column prop="data_size" label="数据大小" align="center">
							</el-table-column>
							<el-table-column prop="index_size" label="索引大小" align="center">
							</el-table-column>
						</el-table>
						<!-- <SqlDiskUsage :id="sql_disk_usage_table" :data="sql_disk_usage_table_data"></SqlDiskUsage> -->
					</div>
				</el-col>
			</el-row>
			<el-row :span="24" class="serve_bottom">

			</el-row>
			<el-row class="serve_center serve_line" :gutter="10">
				<el-col :span="12">
					<div class="serve_center_left">
						<p>读/写比</p>
						<linegraph :id="'bargrapRWRate'" :data="optionRWRate" class="linegraph_mysql"></linegraph>
					</div>
				</el-col>
				<el-col :span="12">
					<div class="serve_center_right">
						<p>缓存命中率</p>
						<linegraph :id="'bargrapCacheHitRate'" :data="optionCacheHitRate" class="linegraph_mysql"></linegraph>
					</div>
				</el-col>
			</el-row>
			<el-row :span="24" class="serve_bottom">
				<div class="serve_bottom_box mlr10">
					<p>响应时间最长的SQL</p>
					<el-table class="table-content" :data="sql_most_response_table_data" border max-height="300px" style="">
						<el-table-column prop="SCHEMA_NAME" label="SCHEMA名称" align="center">
						</el-table-column>
						<el-table-column prop="DIGEST_TEXT" label="SQL语句" align="center">
						</el-table-column>
						<el-table-column prop="AVG_TIMER_WAIT" label="平均等待时间" align="center">
						</el-table-column>
						<el-table-column  prop="COUNT_STAR" label="COUNT_STAR" align="center">
						</el-table-column>
						<el-table-column  prop="FIRST_SEEN" label="最早执行时间" align="center">
						</el-table-column>
						<el-table-column  prop="LAST_SEEN" label="最晚执行时间" align="center">
						</el-table-column>
					</el-table>
					<!-- <SqlMostResponseTime :id="sql_most_response_table" :data="sql_most_response_table_data"></SqlMostResponseTime> -->
				</div>
			</el-row>

		</div>
	</div>

</template>
<script>
	import linegraph from '../network_equipment/visualNetworkEchart/MinutesCpuUtilization.vue';
	import SqlAvgTime from './mysqlEchart/SqlAvgTime.vue'
	import SqlMostResponseTime from "./mysqlEchart/SqlMostResponseTime.vue";
	import SqlDiskUsage from "./mysqlEchart/SqlDiskUsage";

	export default {
		name: 'ViewServe',
		components: {
			SqlAvgTime,
			SqlMostResponseTime,
			SqlDiskUsage,
			linegraph
		},
		data() {
			return {
				port: '3306',
				serveIp: '',
				version_comment: '',
				version: '',
				uptime: '',
				sql_avg_time_table: 'sql_avg_time_table',
				sql_avg_time_table_data: [],
				sql_most_response_table: 'sql_most_response_table',
				sql_most_response_table_data: [],

				sql_disk_usage_table: 'sql_disk_usage_table',
				sql_disk_usage_table_data: [],
				optionRWRate: {
					title: '',
					legendData: [],
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				optionCacheHitRate: {
					title: '',
					legendData: [],
					xAxisData: [],
					seriesData: [],
					animation: true
				},
				monitorTime: '',
				mysqlData: [],
				mysqlDatabase: '',
			}
		},
		computed: {},
		created() {
			this.monitorTime = [this.Format(new Date() - 12 * 60 * 60 * 1000), this.Format(new Date())];
			this.queryOneMysql();
			this.timer = setInterval(() => {
				this.changeQueryHost();
			}, 180000);
		},
		mounted() {},
		methods: {
			formatDate(date) {
			    var date = new Date(date);
			    var YY = date.getFullYear() + '-';
			    var MM = (date.getMonth() + 1 < 10 ? '0' + (date.getMonth() + 1) : date.getMonth() + 1) + '-';
			    var DD = (date.getDate() < 10 ? '0' + (date.getDate()) : date.getDate());
			    var hh = (date.getHours() < 10 ? '0' + date.getHours() : date.getHours()) + ':';
			    var mm = (date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()) + ':';
			    var ss = (date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds());
			    return YY + MM + DD +" "+hh + mm + ss;
			},
			queryOneMysql() {
				this.$http.get(`monitor/api/databases/?db_type=MYSQL&current_page=1&pre_page=1&is_monitor=是`, {
					headers: {
						'token': localStorage.getItem('token')
					}
				}).then((res) => {
					const oneMysqlData = res.data;
					const ip = oneMysqlData.data[0].ip_address;
					const sid = oneMysqlData.data[0].sid;
					this.mysqlDatabase = sid + '/' + ip;
					this.optionData(ip, sid);
					const curTime = Date.parse(this.monitorTime[1]) / 1000;
					const startTime = Date.parse(this.monitorTime[0]) / 1000;
					this.query_history(startTime, curTime, ip);
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			queryMysqlDB(query) {
				if (query !== '') {
					this.$http.get(`monitor/api/databases/search?db_type=MYSQL&query=${query}&is_monitor=是`, {
						headers: {
							'token': localStorage.getItem('token')
						}
					}).then((res) => {
						this.mysqlData = res.data;
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
				const db_name = this.mysqlDatabase.split('/');
				const db_sid = db_name[0];
				const db_ip = db_name[1];
				this.optionData(db_ip, db_sid);
				this.query_history(startTime, curTime, db_ip);
			},
			optionData(db_ip, db_sid) {
				this.$http.get(`monitor/api/databases/monitor/?db_name=MYSQL_${db_ip}_${db_sid}`, {
					headers: {
						'token': this.token
					}
				}).then((res) => {
					console.log(res.data)
					this.port = Number(res.data.PORT);
					this.serveIp = res.data.LOGIC_IP;
					this.uptime = parseInt(res.data.UPTIME / 60 / 60 / 24);
					this.version_comment = res.data.VERSION_COMMENT;
					this.version = res.data.VERSION;

					this.sql_avg_time_table_data = res.data.SQL_AVG_TIME;
					//this.sql_most_response_table_data = res.data.SQL_MOST_RESPONSE_TIME;
					for(var i=0;i<res.data.SQL_MOST_RESPONSE_TIME.length;i++){
						var obj=new Object();
						obj.SCHEMA_NAME=res.data.SQL_MOST_RESPONSE_TIME[i].SCHEMA_NAME;
						obj.DIGEST_TEXT=res.data.SQL_MOST_RESPONSE_TIME[i].DIGEST_TEXT;
						obj.AVG_TIMER_WAIT=res.data.SQL_MOST_RESPONSE_TIME[i].AVG_TIMER_WAIT;
						obj.COUNT_STAR=res.data.SQL_MOST_RESPONSE_TIME[i].COUNT_STAR;
						obj.FIRST_SEEN=this.formatDate(res.data.SQL_MOST_RESPONSE_TIME[i].FIRST_SEEN);
						obj.LAST_SEEN=this.formatDate(res.data.SQL_MOST_RESPONSE_TIME[i].LAST_SEEN);
						this.sql_most_response_table_data.push(obj);
					}
					this.sql_disk_usage_table_data = res.data.SQL_DISK_USAGE;
				}).catch((error) => {
					this.$message.error(JSON.stringify(error.response.data));
				});
			},
			query_history(startTime, curTime, db_ip) {
				this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime +
					`&m=sum:RW_RATIO{logicIp=${db_ip}}`, {
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
					this.optionRWRate.xAxisData = lineXtime;
					this.optionRWRate.seriesData = [{
						name: "R/W",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#d47443'
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
									color: 'rgba(212,116,67, 0.9)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(212,116,67, 0)' // 100% 处的颜色
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
					console.log(error);
					this.$message.error(JSON.stringify(error.response.data));
				});

				this.$http.get(`monitor/api/databases/history/?start=` + startTime + `&end=` + curTime +
					`&m=sum:CACHE_HIT_RATE{logicIp=${db_ip}}`, {
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
					this.optionCacheHitRate.xAxisData = lineXtime;
					this.optionCacheHitRate.seriesData = [{
						name: "缓存命中率",
						type: "line",
						smooth: true,
						symbol: 'circle',
						symbolSize: 3,
						lineStyle: {
							normal: {
								color: '#50d48c'
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
									color: 'rgba(80,212,140, 0.9)' // 0% 处的颜色
								}, {
									offset: 0.8,
									color: 'rgba(80,212,140, 0)' // 100% 处的颜色
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
					console.log(error);
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
				let s = date.getSeconds();
				s = s < 10 ? ('0' + s) : s;
				return y + '-' + MM + '-' + d + ' ' + h + ':' + m + ':' + s;

			}
		},
		beforeDestroy() {
			clearInterval(this.timer);
		}
	}
</script>
<style lang="scss" scoped>
	@import "../../../assets/css/fonts/font.css";
	@import "../../../assets/scss/echarts";
	@import "../../../assets/scss/darkStyle";
	.linegraph_mysql {
		height: 170px;
	}

	.serve_top {
		border-radius: 10px;
		height: 220px;
	}

	.serve_bottom {
		margin: 13px 0;
	}

	.serve_center_left,
	.serve_center_right {
		height: 200px;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_center_left {
		margin: 0;
	}

	.serve_bottom_left,
	.serve_bottom_right {
		height: 390px;
		background: #24273e;
		border-radius: 10px;
	}

	.serve_bottom_box {
		background: #24273e;
		border-radius: 10px;
		padding-bottom: 10px;
	}

	.serve_bottom,
	.serve_bottom_left {
		p {
			color: #03c2ec;
			font-size: 12px;
			padding: 10px 0 0 10px;
			font-weight: 600;
		}
	}

	.serve_top_char {
		height: 70px;
		background: #24273e;
		border-radius: 10px;
	}

	dl {
		.serve_name {
			font-size: 18px;
		}

		dd {
			margin-top: 2px;
		}
	}

	p {
		color: #03c2ec;
		font-size: 12px;
		padding: 10px 0 0 10px;
		font-weight: 600;
	}

	.serve_line {
		margin: 0 5px !important;
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
	/deep/.el-table{
		padding: 10px 0;
	}
	/deep/.el-table th {
		background-color: #2c2f49 !important;
		color: #b08ff9;
		font-weight: normal;
	}
	/deep/ .el-table--border{
		border: none;
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
</style>

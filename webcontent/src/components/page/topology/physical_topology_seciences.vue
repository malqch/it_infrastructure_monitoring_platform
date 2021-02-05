<template>
  <div class="app-container" >
    <div id="torpBox" class="main_view"/>
    <div class="l000_mask">
      <div class="l000_win_device">
        <h5>设备信息</h5>
        <span class="l000_win000_close">+</span>
        <ul id="l000_mach000_info" class="l000_mach000_info">
          <li>设备ID：<span id="machId"/></li>
          <li>设备型号：<span id="machType"/></li>
          <li>设备类型：<span id="machTypeName"/></li>
          <li>设备IP：<span id="machIp"/></li>
        </ul>
        <div class="l000_btnBox">
          <a href="javascript:;" class="btn_control">设备监控</a>
          <a href="javascript:;" class="btn_manage">设备管理</a>
        </div>
      </div>
      <div class="l000_win">
        <h5>链接信息</h5>
        <span class="l000_win000_close">+</span>
        <ul id="l000_link000_info" class="l000_link000_info">
          <li>
            <el-row>
              <el-col :span="5">链接关系：</el-col>
              <el-col :span="19">
                <el-row>
                  <span class="select_value_label">本端:</span>
                  <select class="select_value" style="width:90%;"/>
                </el-row>
                <el-row>
                  <span class="after_value_label">对端:</span><span class="after_value"/>
                </el-row>
              </el-col>
            </el-row>
          </li>
          <li>
            <el-row>
              连接状态：<span class="connection_status">正常</span>
            </el-row>
          </li>
          <li>
            <el-row>链路带宽：<span class="link_bandwidth">50Mb</span></el-row>
          </li>
          <li>
            <el-row>
              链路聚合：<span class="source_if_port_channel"/>
            </el-row>
          </li>
          <li>
            <el-row>链路使用率：<span class="link_used">50Mb</span></el-row>
          </li>
          <li>
            <el-row>IP：<span class="source_if_ip"/></el-row>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Physicstopology',
  data() {
    return {
      'resData': null,
      'dataFromRequest': {},
      'vcenterInfo': [],
      'deviceid': '',
      'all_data_init': null
    }
  },
  mounted() {
    // 加载列表数据
      this.getMapList()
  },
  // 方法集合
  methods: {
    getTorpData(resData) {
      const _self = this
      const rslData = {
        'nodes': [],
        'links': [],
        'lines': [],
        'text': []
      }
      resData.topology[0].node.forEach((v,i) => {
        const limitRow = 5
         rslData.nodes.push({
           'id': 'l000_torp000_' + v['node-id'],
           'x': 110 * (i % limitRow+0.4),
           'y': 120 * (Math.floor(i / limitRow)+0.5),
           'name': v['node-id'],
           'background_id': v['device-type'] + (v['devicegroup-type'] ? '_G' : ''),
           'background': _self.getBkgd(v['device-type'], v['devicegroup-type']),
           'otherClassName': v['devicegroup-type'],
           'diy_attr': {},
           'oraData': v
         })
      })
      resData.topology[0].link.forEach((v, i) => {
        if (v['bandwidth'] === undefined) {
          v['bandwidth'] = ''
        }
        rslData.links.push({
          'id': 'l000_line000_' + new Date().getTime() + '' + i,
          'name': '',
          'source': 'l000_right000_' + v.source['source-node'] + '000_' + i,
          'target': 'l000_left000_' + v.destination['dest-node'] + '000_' + i,
          'color': v.status === 'Connected' ? '#03b1f4' : '#ff5e50',
          'isDash': false,
          'arrowType': v.arrowType,
          'diy_attr': { 'link-id': v['link-id'], 'all_data': this.resData, 'bandwidth': v['bandwidth'], 'bandwidth-used': v['bandwidth-used'], 'status': v['status'], 'all_data_init': this.all_data_init }
        })
      })
      return rslData
    },
    getBkgd(type, gType) {
      if (type === 'defualt') {
          if (gType === 'stack') {
              return "url('../../../assets/img/topological/switch2.png')"
          } else {
//              return "url('../../../assets/img/topological/switch_to.png')"
          }
      }else if (type === 'FW') {
        if (gType === 'stack') {
          return "url('../../../assets/img/fw2.png')"
        } else {
          return "url('../../../assets/img/fw_to.png')"
        }
      }else if (type === 'Router') {
        if (gType === 'stack') {
          return "url('../../../assets/img/router_tolo.png')"
        } else {
          return "url('../../../assets/img/router_to_tolo.png')"
        }
      }else if (type === 'Switch') {
        if (gType === 'stack') {
          return "url('../../../assets/img/switch2.png')"
        } else {
          return "url('../../../assets/img/switch_to.png')"
        }
      }else{
            if(gType === 'stack'){
                return "url('../../../assets/img/unknow.png')"
            }else{
                return "url('../../../assets/img/unknow_to.png')"
            }
        }
    },
    getMapList() {
        this.$http.get(`phy_topo/link_topo`, {
            headers:
                {'token':localStorage.getItem('token'),
				'responseType':'arraybuffer',
				'Content-Type':'application/json;charset=UTF-8',
				'Accept':'application/json;charset=UTF-8'}
        }).then((response) => {
            if(response.data!=null){
                if (response.data.msgcode === 0) {
                    this.all_data_init = JSON.parse(JSON.stringify(response.data.data));
                    this.dataFromRequest = JSON.parse(JSON.stringify(response.data.data));
                    for (let index = 0; index < this.dataFromRequest.topology[0].node.length; index++) {
                        const element = this.dataFromRequest.topology[0].node[index]
//                        if (!element.hasOwnProperty('device-family')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "device-family")) {
                            // element.device-family = 'test'
                            this.dataFromRequest.topology[0].node[index]['device-family'] = 'defualt.000000'
                            // console.log('zzzzzzzzzz', JSON.stringify(this.dataFromRequest.topology[0].node[index]))
                        }
//                        if (!element.hasOwnProperty('devicegroup-type')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "devicegroup-type")) {
                            this.dataFromRequest.topology[0].node[index]['devicegroup-type'] = 'defualt'
                        }
//                        if (!element.hasOwnProperty('device-type')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "device-type")) {
                            this.dataFromRequest.topology[0].node[index]['device-type'] = 'defualt'
                        }
//                        if (!element.hasOwnProperty('connection-type')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "connection-type")) {
                            this.dataFromRequest.topology[0].node[index]['connection-type'] = 'defualt'
                        }
//                        if (!element.hasOwnProperty('host')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "host")) {
                            this.dataFromRequest.topology[0].node[index]['host'] = '0.0.0.0'
                        }
//                        if (!element.hasOwnProperty('status')) {
                        if (!Object.prototype.hasOwnProperty.call(element, "status")) {
                            this.dataFromRequest.topology[0].node[index]['status'] = 'defualt'
                        }
                    }
                    this.dataFromRequest.topology[0].node.forEach((v) => {
                        const reg = new RegExp('\\.', 'g')
                        v['node-id'] = v['node-id'].replace(reg, '-')
                        const reg2 = new RegExp(':', 'g')
                        v['node-id'] = v['node-id'].replace(reg2, '-')
                    })
                    this.dataFromRequest.topology[0].link.forEach((v) => {
                        const reg = new RegExp('\\.', 'g')
                        v.source['source-node'] = v.source['source-node'].replace(reg, '-')
                        v.destination['dest-node'] = v.destination['dest-node'].replace(reg, '-')
                        const reg4 = new RegExp(':', 'g')
                        v.source['source-node'] = v.source['source-node'].replace(reg4, '-')
                        v.destination['dest-node'] = v.destination['dest-node'].replace(reg4, '-')
                    })
                    this.resData = this.dataFromRequest;
                    const _self = this;
                    const torpMap = new TopologyMap({ mainBoxId: 'torpBox',canvasId: 'canvas_1', 
					couldEdit: false, onlyDrag: true, leftViewShow: false, rightViewShow: false })
					console.log(_self.getTorpData(_self.resData))
                    torpMap.setTorpData(_self.getTorpData(_self.resData));
                  $('.l000_torp000_element').on('click', function() {
                   if ($(this).attr('data-win')) {
                       let data = JSON.parse($(this).attr('data-win'));
                       $('#machId').text(data.machId)
                       if (data.machType === 'undefined()') {
                            $('#machType').text('')
                       } else {
                            $('#machType').text(data.machType)
                       }
                            $('#machTypeName').text(data.machTypeName)
                       if (data.host === '0.0.0.0') {
                            $('#machIp').text('')
                       } else {
                            $('#machIp').text(data.host)
                       }
                       const curWwwPath=window.document.location.href;
                       const localhostPaht=curWwwPath.split('#');
                       if(data.machTypeName=='FW' || data.machTypeName=='Switch' || data.machTypeName=='Router'){
                           $('.btn_manage')
                               .attr('href', localhostPaht[0]+'#/asset/network')
                               .attr('target','_blank')
                               .css({ 'background-color': '#409EFF' }).attr('disabled', false);
                       }else{
                           $('.btn_manage').css({ 'background-color': '#ccc' }).attr('disabled', true);
                       }
                   if(data.machTypeName=="unknow" || data.host==""){
                       $('.btn_control').css({ 'background-color': '#ccc' }).attr('disabled', true)
                   }else{
                       if(data.machTypeName=='FW'){
                           $('.btn_control')
                               .attr('href', localhostPaht[0]+'#/monitor/h3cfireWall_visualize?ip='+data.host+ '&device_type=' + data.machTypeName + '&name=' + data.machId)
                               .attr('target','_blank')
                               .css({ 'background-color': '#409EFF' }).attr('disabled', false)
                       }
                       if(data.machTypeName=='Switch' || data.machTypeName=='Router'){
                           $('.btn_control')
                               .attr('href', localhostPaht[0]+'#/monitor/network_visualize?ip='+data.host+'&device_type='+data.machTypeName+'&name='+data.machId)//
                               .attr('target','_blank');
                           $('.btn_control').css({ 'background-color': '#409EFF' }).attr('disabled', false)
                       }

                   }
                   $('.l000_win').hide()
                   $('.l000_win_device').show()
                   // $('.l000_mask').fadeIn()
                   }
                   })
                   $('.l000_win000_close').on('click', function() {
                   $('.l000_mask').hide()
                   })
                } else {
                    this.$message.warning(response.data.msg)
                }
            }
        }).catch( (error)=> {
            console.log(error);
            this.$message.error(JSON.stringify(error.response.data));
        });


    }
  }
}
</script>

<style>

  html, body, div, span, object, iframe,h1, h2, h3, h4, h5, h6, p, blockquote, pre,abbr, address, cite, code,del, dfn, em, img, ins, kbd, q, samp,small, strong, sub, sup, var,b, i,dl, dt, dd, ol, ul, li,fieldset, form, label, legend,table, caption, tbody, tfoot, thead, tr, th, td,article, aside, canvas, details, figcaption, figure, footer, header, hgroup, menu, nav, section, summary,time, mark, audio, video{margin:0;padding:0;border:0; outline:0;vertical-align:baseline;font-style: normal;}
  html,ul,li,ol,p,h1,h2,h3,h4,h5,h6,dl,dt,dd{margin:0;padding:0;}
  html{font-family:Tahoma,Arial,Roboto,”Droid Sans”,”Helvetica Neue”,”Droid Sans Fallback”,”Heiti SC”,sans-self,Microsoft YaHei;box-sizing:border-box;-webkit-font-smoothing:antialiased;text-shadow:1px 1px 1px rgba(0,0,0,0.004);background: #fff;}/*使字体更加清晰*/
  /*html,body{width: 100%;height: 100%;min-width: 320px;overflow: hidden; }!* 页面背景宽高设置 *!*/
  *{ -webkit-overflow-scrolling: touch; overflow-scrolling: touch;-webkit-tap-highlight-color: rgba(0,0,0,0);-webkit-tap-highlight-color: transparent; /* For some Androids */  }
  li{list-style:none;	}
  a{text-decoration:none;color:initial; }
  img{border:none;}
  /*input,button,select,textarea{outline:none; !*cursor: pointer;*! -webkit-appearance: none;border-radius: 0;padding: 0;}!*清除input，textarea输入框的默认样式*!*/
  input{ cursor: pointer;border:solid 1px rgba(0,0,0,0.1); }
  input[type=button],input[type=submit],input[type=file],button{ cursor: pointer; -webkit-appearance: none;border: none;text-indent:0;}
  textarea{resize:none}/*清除input，textarea输入框的默认样式*/
  /*input中placeholder颜色*/
  input::-webkit-input-placeholder { color: #999;letter-spacing: 0; } /* WebKit browsers */
  input:-moz-placeholder { color: #999;letter-spacing: 0;  } /* Mozilla Firefox 4 to 18 */
  input::-moz-placeholder {  color: #999;letter-spacing: 0;  } /* Mozilla Firefox 19+ */
  input:-ms-input-placeholder { color: #999;letter-spacing: 0;  }/* Internet Explorer 10+ */
  .text-overflow{text-overflow:ellipsis;white-space:nowrap;overflow:hidden; }/* 字体溢出省略样式 */
  .main_view{width: 100%;height:calc(100% - 66px);/*border: 1px solid #53adff;*/margin-top: 10px;}
  .l000_view{height:100%;float: left;box-sizing: border-box;position: relative;}
  .l000_drag000_element{width: 70px;height: 70px;
    /*border: solid 2px #53adff;*/
    border-radius:8px;float: left;margin: 30px 0 30px 16%;cursor:move;position: relative;}
  .l000_drag000_element>p{position: absolute;top:71px;left:-9px;text-align: center;font-size: 12px;width: 80px;padding:4px;border-radius:4px;color: #fff;
    /*background: rgba(56, 134, 198, 0.8);*/
    word-break:break-word;}
  .l000_torp000_element{width: 80px;height: 80px;position: absolute;margin:0;}
  .l000_torp000_element>.l000_drag000_element{margin: 0;}
  .l000_opera000_view{position: relative;
    /*overflow: auto;*/
  }
  .l000_torp000_info000_window{position: absolute;width: 40%;height: 40%;background: rgba(0,0,0,0.8);border-radius: 4px;color:#fff;top:0;left: 0;display: none;padding: 2%;box-sizing: border-box;z-index: 2000;border-radius:4px;}
  .l000_torp000_info000_window>p{margin-bottom: 18px;}
  .l000_torp000_element.l000_left000_text,.l000_torp000_element.l000_left000_text>div{width: auto;height: auto;text-align: center;border: none;font-size: 12px;line-height: 12px;color: #53adff;}
  .l000_torp000_element.l000_left000_text>div{cursor: move;}
  .l000_torp000_element.l000_left000_text>div{padding: 20px;}
  .l000_left000_text>div>span{position: absolute;right: 2px;top: 2px;width: 16px;height: 16px;text-align: center;background: #53adff;color: #fff;line-height: 16px;font-size: 14px;transform: rotate(45deg);border-radius: 100%;cursor: pointer;display: none;}
  .l000_left000_text>div>input{display: none;border: none;width: auto;height: auto;outline:none; -webkit-appearance: none;border-radius: 0;padding: 0;}
  .l000_torp000_dot{position: absolute;width: 10px;height: 10px;background: #fff;border-radius: 100%;border: solid 2px #53ADFF;z-index:-3;cursor:default;}
  .l000_torp000_dot:hover{border: solid 2px #3d7fbb; }
  .l000_torp000_dot.l000_dot000_active{border: solid 2px #3d7fbb;background:#3d7fbb;}
  .l000_del000_torp{position: absolute;right:2px;top:2px;width: 16px;height:16px;text-align:center;line-height:15px;font-size:12px;background: #3d7fbb;color: #fff;border-radius: 10px;transform: rotate(45deg);opacity: 0.6;cursor: pointer;display: none;z-index: 2;}
  .l000_right000_box{width: 100%;height: 100%;overflow: auto;}
  .l000_right000_box>ul,.l000_left000_drag000_box{width: 100%;height: auto;overflow: hidden;min-width: 200px;padding-bottom: 30px;}
  .l000_left000_drag000_box{min-width: unset;}
  .l000_title{width: 100%;height: 30px;background:#53adff;text-align: center;line-height: 30px;color: #fff;position: relative;cursor: pointer;}
  .l000_title::after{content:'';position: absolute;width:6px;height:6px;right:6%;top:13px;border-right:solid 1px #fff;border-bottom:solid 1px #fff;transform: rotate(-45deg);transform-origin: center center;}
  .l000_title.l000_open::after{transform: rotate(45deg);top:10px;}
  .l000_element000_box label,.l000_line000_box label{font-size: 12px;color: #666;}
  .l000_element000_box li,.l000_line000_box li{margin-top: 20px;padding:0 4%;box-sizing: border-box;}
  .l000_element000_box li.l000_nomargin,.l000_line000_box li.l000_nomargin{margin-top: 0px;}
  .l000_diy000_style>div{width: 160px;height: 160px;background: #fff;border: solid 1px #ccc;margin: 20px auto;position: relative;}
  .l000_diy000_style>div p{font-size: 14px;text-align: center;}
  .l000_diy000_style>div span{display: block;background: #afafaf;width: 100px;height: 100px;margin: 15px auto;}
  .l000_diy000_style>div input{display: block;width: 100%;height: 30px;position: absolute;bottom:0;left:0;z-index: 2;opacity: 0}
  .l000_diy000_style>div b{display: block;width: 100%;height: 30px;position: absolute;bottom:0;left:0;background:#53adff;color:#fff;text-align:center;font-size:12px;line-height:30px;z-index: 1;}
  .l000_diy000_input000_box{width: 100%;position: relative;}
  .l000_diy000_input000_box input{width: 40%;}
  .l000_add000_diy000_style p{display: block;position: relative;height:20px;cursor: pointer;border: solid 1px #53adff;color: #53adff;width: 100%;padding: 4px 0;border-radius:4px;text-align:center;font-size:12px;line-height:20px;}
  .l000_delete000_diy000_style{width: 20px;height: 20px;text-align: center;line-height: 18px;font-weight: bold;font-size: 16px;transform: rotate(45deg);color: #fff;background: #8e3104;cursor: pointer;border-radius: 100%;position: absolute;right: 4%;top: 2px;}
  /*.l000_drag000_element.l000_element000_checked{border: solid 2px #2a7dc8;}*/
  .l000_diy000_color{overflow: hidden;}
  .l000_diy000_color *{float: left}
  .l000_diy000_color input{width: 120px;}
  .l000_diy000_color>div{margin-top: 20px;}
  .l000_tool000_btn{width: 40px;height: 40px;line-height: 40px;color: #666;border:solid 1px #333;text-align: center;font-size: 24px;float: left;margin: 20px 0 0 6%;cursor: pointer;}
  .l000_tool000_btn.l000_left000_active{color: #53adff;border: solid 1px #53adff}
  #l000_color{display:block;width: 20px;height: 20px;background: #ccc;margin-right: 40px;position: relative;}
  #l000_color::after{content: '#';position: absolute;right: -40px;top: 50%;margin-top: -10px;width: 20px;height: 20px;line-height: 20px;text-align: center;}
  #l000_inputButton,.l000_inputButton,#l000_outputButton{position: absolute;top:10px;width: 100px;height: 24px;font-size: 12px;background: #53adff;color: #fff;}
  #l000_inputButton,.l000_inputButton{right:10px;cursor: pointer;}
  #l000_inputButton{z-index: 2;}
  #l000_outputButton{right: 80px;}
  .l000_torp000_element.stack::after{
    content: 'stack';
    position: absolute;
    right: 11px;
    top: 2px;
    line-height: 4px;
    height: 5px;
    padding: 4px 8px;
    font-size: 10px;
    color: #fff;
    background: #5481d2;
    border-radius: 0 6px 0 8px;
  }
  .l000_mask{
    position: absolute;
    width: 100%;
    height: 100%;
    /*background:rgba(0,0,0,0.6);*/
    top:0;
    left: 0;
    z-index: 99;
    display: none;
  }
.l000_win {
    width: 520px;
    /*height: 85vh;*/
    height:265px;
    position: absolute;
    left: 50%;
    margin-left: -250px;
    top: 5%;
    background:#032d57;
    border-radius: 8px;
    border: 2px solid #53adff;
    -webkit-box-sizing: border-box;
    box-sizing: border-box;
    padding: 1%;
    color: #d8e2f3;
    /*overflow-y:scroll ;*/
}
.l000_win_device{
  width: 480px;
  height: 238px;
  position: absolute;
  left: 50%;
  margin-left: -250px;
  top: 10%;
  background: #032d57;
  border-radius: 8px;
  border: 2px solid #032d57;
  box-sizing: border-box;
  padding: 1%;
  color: #d8e2f3;
}
  .l000_win h5{
    display: block;
    margin-bottom: 12px;
    color: #d8e2f3;
    font-size: 20px;
  }
    .l000_win_device h5{
    display: block;
    margin-bottom: 30px;
    color: #c6d1df;
    font-size: 20px;
  }
  .l000_win .l000_win000_close{
    position: absolute;
    width: 30px;
    height: 30px;
    line-height: 28px;
    text-align: center;
    color: #c6d1df;
    border-radius: 100%;
    border: 1px solid  #c6d1df;
    transform: rotate(45deg);
    right: 4%;
    top:4%;
    font-size: 31px;
    cursor: pointer;
  }
    .l000_win_device .l000_win000_close{
    position: absolute;
    width: 30px;
    height: 30px;
    line-height: 28px;
    text-align: center;
    color: #c6d1df;
    border-radius: 100%;
    border: 1px solid  #c6d1df;
    transform: rotate(45deg);
    right: 4%;
    top:4%;
    font-size: 31px;
    cursor: pointer;
  }
  .l000_win ul>li {margin-bottom: 0px;font-size: 16px;}
  .l000_win ul{
    width: 100%;
    overflow-y: auto;
  }
.l000_btnBox{
    position: absolute;
    bottom: 5%;
    right: 4%;
    width: 50%;
    overflow: hidden;
  }
  .l000_btnBox a{
    display: block;
    float: right;
    width: 40%;
    margin-left: 5%;
    height: 40px;
    line-height: 40px;
    background: #53adff;
    text-align: center;
    cursor: pointer;
    color: #fff;
    font-size: 18px;
    border-radius: 4px;
  }
  .app-container{
   padding: 0 0 0 20px;
    height: 100%;
  }

  canvas.l000_pointer{
    cursor: pointer!important;
  }
  .monitoring_iframe{
    width: 1169px;
    height: 62vh;
  }
.btn_reset{
  margin-bottom: 5px;
}
.select_value_label{
  color: #409EFF;
}
.after_value_label{
   color: red;
}

.after_value{
   font-size: 18px;
}
  .l000_mach000_info{
    line-height: 26px;
  }
  .l000_link000_info{
    line-height: 26px;
  }
</style>


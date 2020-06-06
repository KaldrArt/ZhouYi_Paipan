import {XinPaiGeju} from './geju.coffee'
import {Bazi} from '../basic/bazi.coffee'
import {XinPaiBasic} from './xinpaibasic.coffee'
import _ from 'lodash'

class BaiShenLun
	yang:['正印','劫财','伤官','正财','正官']
	yin:['偏印','比肩','食神','偏财','偏官']
	relation:[1,1,-1,-1,-1]
	NianGan:{}
	YueGan:{}
	RiZhi:{}
	ShiGan:{}
	
	setBasicLiuqin:()=>
		@liuqin=
			zhengguan:
				name:"正官"
				zhu:""
				yongji:0
				yinyang:1
			pianguan:
				name:"偏官"
				zhu:""
				yongji:0
				yinyang:-1
			zhengcai:
				name:"正财"
				zhu:""
				yongji:0
				yinyang:1
			piancai:
				name:"偏财"
				zhu:""
				yongji:0
				yinyang:-1
			zhengyin:
				name:"正印"
				zhu:""
				yongji:0
				yinyang:1
			pianyin:
				name:"偏印"
				zhu:""
				yongji:0
				yinyang:-1
			shishen:
				name:"食神"
				zhu:""
				yongji:0
				yinyang:-1
			shangguan:
				name:"伤官"
				zhu:""
				yongji:0
				yinyang:1
			bijian:
				name:"比肩"
				zhu:""
				yongji:0
				yinyang:-1
			jiecai:
				name:"劫财"
				zhu:""
				yongji:0
				yinyang:1
	
	constructor:(@bazi,@gejuOb)->
		@setBasicLiuqin()
		@XinPaiBasic=new XinPaiBasic()
		# 日支六亲用忌
		@RiZhiYongJi()
		# 月干用忌
		@YueGanYongJi()
		# 年干用忌
		@NianGanYongJi()
		# 时干用忌
		@ShiGanYongJi()
		# 设置未透出的六亲所寄的天干
		@setHiddenLiuQin()
		# 判断未透出的六亲的用忌
		@judgeUnsetLiuqinYongji()
	
	###*
	 * 判断一个天干的用忌
	 * @param  {string} name 天干位置名称
	 * @return {number}      1用神，-1忌神
	###
	judgeYongJi:(name)=>
		switch @gejuOb.geju
			when '从弱'
				if @gejuOb.gejuRelation[name]>0 then @[name].yongji=-1 else @[name].yongji=1
			when '从旺'
				if @gejuOb.gejuRelation[name]<0 then @[name].yongji=-1 else @[name].yongji=1
			when '身弱'
				if name=='RiZhi'
					if @gejuOb.gejuRelation[name]>0 then @[name].yongji=1 else @[name].yongji=-1
				else
					if @gejuOb.gejuRelation[name]>0 
						if @gejuOb.gejuYouli[name]>0 then @[name].yongji=1 else @[name].yongji=-1
					else if @gejuOb.gejuRelation[name]<0
						if @gejuOb.gejuYouli[name]<0 then @[name].yongji=1 else @[name].yongji=-1
			when '身旺'
				if name=='RiZhi'
					if @gejuOb.gejuRelation[name]<0 then @[name].yongji=1 else @[name].yongji=-1
				else
					if @gejuOb.gejuRelation[name]<0 
						if @gejuOb.gejuYouli[name]>0 then @[name].yongji=1 else @[name].yongji=-1
					else if @gejuOb.gejuRelation[name]>0
						if @gejuOb.gejuYouli[name]<0 then @[name].yongji=1 else @[name].yongji=-1
		@[name].yongji
	
	setLiuQinObject:(name,zhu,yongji)=>
		liuqinOb=_.find @liuqin,(item)=>item.name==name
		liuqinOb.zhu=zhu
		liuqinOb.yongji=yongji
	
	###*
	 * 找到没有被设置的六亲
	 * @return {list} 六亲列表
	###
	getUnsetLiuQin:()=>
		result=[]
		_.map @liuqin,(value,key)=>
			if value.yongji==0
				result.push
					key:key
					name:value.name
					yinyang:if @yang.indexOf(value.name)>=0 then 1 else -1
		result
	
	###*
	 * 设置一个未透的六亲的参考六亲
	 * @param {list} unsetLiuqin 未设置的六亲
	 * @param {number} yinyang     -1阴，1阳
	 * @param {string} zhu         天干的位置名称
	###
	setZhuForUnsetLiuQin:(unsetLiuqin,yinyang,zhu)=>
		_.map unsetLiuqin,(item)=>
			if item.yinyang==yinyang
				@liuqin[item.key].zhu=zhu
				@liuqin[item.key].reference=@[zhu].shishen
				@liuqin[item.key].referenceYinyang=if @yang.indexOf(@[zhu].shishen)>=0 then 1 else -1
	###*
	 * 判断一个未透出的六亲的用忌
	###
	judgeUnsetLiuqinYongji:()=>
		_.map @liuqin,(item)=>
			if item.reference
				referencePosition=if item.referenceYinyang>0 then @yang.indexOf item.reference else @yin.indexOf item.reference
				itemPosition=if item.yinyang>0 then @yang.indexOf item.name else @yin.indexOf item.name
				# 参考六亲与当前需要判断的六亲阴阳相同
				if item.referenceYinyang==item.yinyang
					wangshuai=@liuqinWangshuaiWithoutYinyang referencePosition,itemPosition
				# 参考六亲与当前需要判断的六亲阴阳不同
				else
					wangshuai=@liuqinWangshuaiWithYinyang (@liuqinWangshuaiWithoutYinyang referencePosition,itemPosition),false
				#console.log item.name,wangshuai
				item.yongji=@yongji item.name,item.yinyang,wangshuai
	###*
	 * 用忌
	 * @param  {string} shishen   六亲的名称
	 * @param  {number} yinyang   -1阴，1阳
	 * @param  {boolean} wangshuai 旺衰
	 * @return {number}           1用神，-1忌神
	###
	yongji:(shishen,yinyang,wangshuai)=>
		position=if yinyang>0 then @yang.indexOf shishen else @yin.indexOf shishen
		relation=@relation[position]
		switch @gejuOb.geju
			when '从旺','身弱' # 帮扶的越旺越好，克制的越弱越好
				if (relation>0 and wangshuai) or (relation<0 and !wangshuai) then 1 else -1
			when '从弱','身旺' # 帮扶的越弱越好，克制的越旺越好
				if (relation<0 and wangshuai) or (relation>0 and !wangshuai) then 1 else -1
	###*
	 * 根据阴阳再次判断旺衰
	 * @param  {[type]} wangshuai    [description]
	 * @param  {[type]} yinyangYizhi [description]
	 * @return {[type]}              [description]
	###
	liuqinWangshuaiWithYinyang:(wangshuai,yinyangYizhi)=>
		if yinyangYizhi then wangshuai else !wangshuai

	###*
	 * 根据第二个六亲的位置，判断这个六亲在第一个六亲旺时的旺衰
	 * @param  {number} liuqin1 第一个六亲位置
	 * @param  {number} liuqin2 第二个六亲位置
	 * @return {boolean}         第二个六亲的旺衰，true旺，false弱
	###
	liuqinWangshuaiWithoutYinyang:(liuqin1,liuqin2)=>
		#console.log liuqin1,liuqin2
		# 如果第二个六亲被第一个生，那么旺
		if (liuqin1+1)%5==liuqin2 then true
		# 如果第二个六亲和第一个六亲一样，那么旺
		else if liuqin1%5==liuqin2 then true
		# 其他情况，第二个六亲弱
		else false

	###*
	 * 设置为透出的六亲的参考六亲
	###
	setHiddenLiuQin:()=>
		unsetLiuqin=@getUnsetLiuQin()
		#console.log unsetLiuqin
		# 月干、时干两个六亲阴阳一致
		if @YueGan.shishenYinyang==@ShiGan.shishenYinyang
			#console.log '月干、时干两个六亲阴阳一致'
			if @bazi.gender.id==1
				@setZhuForUnsetLiuQin unsetLiuqin,1,'YueGan'
				@setZhuForUnsetLiuQin unsetLiuqin,-1,'ShiGan'
			else
				@setZhuForUnsetLiuQin unsetLiuqin,-1,'YueGan'
				@setZhuForUnsetLiuQin unsetLiuqin,1,'ShiGan'
		# 月干、时干两个六亲阴阳不一致
		else
			#console.log '月干、时干两个六亲阴阳不一致'
			if @YueGan.shishenYinyang>0
				@setZhuForUnsetLiuQin unsetLiuqin,1,'YueGan'
				@setZhuForUnsetLiuQin unsetLiuqin,-1,'ShiGan'
			else
				@setZhuForUnsetLiuQin unsetLiuqin,1,'ShiGan'
				@setZhuForUnsetLiuQin unsetLiuqin,-1,'YueGan'


	YueGanYongJi:()=>
		@YueGan.shishen=@bazi.RiGan.shiShen @bazi.YueGan.name
		@YueGan.name="月干"
		@YueGan.shishenYinyang=if @yang.indexOf(@YueGan.shishen)>=0 then 1 else -1
		@setLiuQinObject @YueGan.shishen,"YueGan",@judgeYongJi 'YueGan'
	
	ShiGanYongJi:()=>
		@ShiGan.name="时干"
		@ShiGan.shishen=@bazi.RiGan.shiShen @bazi.ShiGan.name
		@ShiGan.shishenYinyang=if @yang.indexOf(@ShiGan.shishen)>=0 then 1 else -1
		@setLiuQinObject @ShiGan.shishen,"ShiGan",@judgeYongJi 'ShiGan'
	
	NianGanYongJi:()=>
		@NianGan.name='年干'
		@NianGan.shishen=@bazi.RiGan.shiShen @bazi.NianGan.name
		NianGanToYueGan=1
		if @XinPaiBasic.tianganWangshuai @bazi.YueGan,@bazi.NianGan then NianGanToYueGan=1 else NianGanToYueGan=-1
		@NianGan.yongji= NianGanToYueGan*@YueGan.yongji
		@NianGan.shishenYinyang=if @yang.indexOf(@NianGan.shishen)>=0 then 1 else -1
		@setLiuQinObject @NianGan.shishen,"NianGan",@NianGan.yongji
	
	RiZhiYongJi:()=>
		@RiZhi.name='日支'
		@judgeYongJi 'RiZhi'

exports.BaiShenLun=BaiShenLun




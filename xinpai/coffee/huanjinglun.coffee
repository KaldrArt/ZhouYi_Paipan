import {XinPaiBasic} from './xinpaibasic.coffee'
import {XinPaiGeju} from './geju.coffee'
import {Bazi} from '../basic/bazi.coffee'
import {BaiShenLun} from './baishenlun.coffee'
import _ from 'lodash'
import {MuKuLun} from './mukulun.coffee'

# -----------------------------------
# 环境论
# 
# 环境论的本质是，根据力的作用原理，对每个字的旺弱做判断。
# 判断好旺弱之后，根据忌用神，来判断每一个字的吉凶。
# 不需要判断外部环境、内部环境天干地支之间的关系

class HuanJingLun
	tiangan:['NianGan','YueGan','RiGan','ShiGan']
	dizhi:['NianZhi','YueZhi','RiZhi','ShiZhi']
	zheng:["zhengguan",'zhengyin','zhengcai','jiecai','shangguan']
	pian:['piancai','pianguan','pianyin','bijian','shishen']
	liuqin:{}
	# 男性正六亲左侧为社会环境，右侧为家庭环境，偏六亲相反
	# 女性和男性的全部相反
	# 1 男性，正六亲； 0 女性； -1 偏六亲
	genderMap:
		0:
			zheng:
				social:1
				family:-1
			pian:
				social:-1
				family:1
		1:
			zheng:
				social:-1
				family:1
			pian:
				social:1
				family:-1
	#对此，李老师专门说过，无论男女和正偏其工作环境都在月，内部环境都在日。而时上的六亲其工作环境在日，内部环境在月。
	#我修正后，你第一个问题，日为工作环境，月为内部环境。第二个问题，月为工作环境，日为内部环境。
	specialMap:
		# 六亲在年柱
		0:
			0:
				pian:
					social:2
					family:1
				zheng:
					social:1
					family:2
			1:
				pian:
					social:1
					family:2
				zheng:
					social:2
					family:1
		# 六亲在时柱
		3:
			0:
				zheng:
					social:1
					family:2
				pian:
					social:2
					family:1
			1:
				zheng:
					social:2
					family:1
				pian:
					social:1
					family:2

	constructor:(@bazi,@baishenlun)->
		@MuKuLun=new MuKuLun()
		@XinPaiBasic=new XinPaiBasic()
		@liuqin=@baishenlun.liuqin
		@buildHuanjingForLiuqin()

	
	initEnvForALiuqin:(key)=>
		#console.log "===================================================="
		liuqin=@liuqin[key]
		#console.log liuqin.name,liuqin.yongji

		positionOfLiuqinWai=@tiangan.indexOf liuqin.zhu
		positionOfLiuqinNei=positionOfLiuqinWai
		positionOfLiuqinWaiSocial=@getLiuqinWaiSocial liuqin.yinyang,positionOfLiuqinWai
		positionOfLiuqinWaiFamily=@getLiuqinWaiFamily liuqin.yinyang,positionOfLiuqinWai
		positionOfLiuqinNeiSocial=positionOfLiuqinWaiSocial
		positionOfLiuqinNeiFamily=positionOfLiuqinWaiFamily
		neiYongji=liuqin.yongji*@getLiuqinNeiYongji liuqin
		
		#console.log "===================================================="
		#console.log @bazi[@tiangan[positionOfLiuqinWai]].name,@bazi[@dizhi[positionOfLiuqinWai]].name
		#console.log "内环境 #{neiYongji}"

		liuqin.env=
			wai:
				ganzhi:@bazi[@tiangan[positionOfLiuqinWai]].name
				position:positionOfLiuqinWai
				positionName:@tiangan[positionOfLiuqinWai]
				yongji:liuqin.yongji
				social:
					ganzhi:@bazi[@tiangan[positionOfLiuqinWaiSocial]].name
					position:positionOfLiuqinWaiSocial
					positionName:@tiangan[positionOfLiuqinWaiSocial]
					yongji:liuqin.yongji*@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinWaiSocial,'wai'
				family:
					ganzhi:@bazi[@tiangan[positionOfLiuqinWaiFamily]].name
					position:positionOfLiuqinWaiFamily
					positionName:@tiangan[positionOfLiuqinWaiFamily]
					yongji:liuqin.yongji*@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinWaiFamily,'wai'
			nei:
				ganzhi:@bazi[@dizhi[positionOfLiuqinNei]].name
				position:positionOfLiuqinNei
				positionName:@dizhi[positionOfLiuqinNei]
				yongji:neiYongji
				social:
					ganzhi:@bazi[@dizhi[positionOfLiuqinNeiSocial]].name
					position:positionOfLiuqinNeiSocial
					positionName:@dizhi[positionOfLiuqinNeiSocial]
					yongjiToNei:@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinNeiSocial,'nei'
					yongjiFromNei:neiYongji*@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinNeiSocial,'nei'
				family:
					ganzhi:@bazi[@dizhi[positionOfLiuqinNeiFamily]].name
					position:positionOfLiuqinNeiFamily
					positionName:@dizhi[positionOfLiuqinNeiFamily]
					yongjiFromNei:neiYongji*@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinNeiFamily,'nei'
					yongjiToNei:@yongjiOfLiuqinHuanjing liuqin,positionOfLiuqinNeiFamily,'nei'
		liuqin.env.nei.social.yongjiToSocial=@tongzhuDizhiToTiangan positionOfLiuqinNeiSocial
		liuqin.env.nei.social.yongjiFromSocial = liuqin.env.wai.social.yongji * liuqin.env.nei.social.yongjiToSocial
		liuqin.env.nei.family.yongjiToFamily = @tongzhuDizhiToTiangan positionOfLiuqinNeiFamily
		liuqin.env.nei.family.yongjiFromFamily = liuqin.env.wai.family.yongji * liuqin.env.nei.family.yongjiToFamily
		liuqin.env.nei.social.kongwang=true if @bazi.kongwang.indexOf(liuqin.env.nei.social.ganzhi)>=0 and liuqin.env.nei.social.position!=0
		liuqin.env.nei.family.kongwang=true if @bazi.kongwang.indexOf(liuqin.env.nei.family.ganzhi)>=0 and liuqin.env.nei.family.position!=0
		liuqin.env.nei.kongwang=true if @bazi.kongwang.indexOf(liuqin.env.nei.ganzhi)>=0 and liuqin.env.nei.position!=0
	###*
	 * 同柱地支与天干的关系
	 * @param  {number} position 天干的位置，0-3
	 * @return {number}          1旺，-1忌
	###
	tongzhuDizhiToTiangan:(position)=>
		dizhi=@bazi[@dizhi[position]]
		tiangan=@bazi[@tiangan[position]]
		result=@XinPaiBasic.wangshuaiWithMukuLun tiangan,dizhi,position==1
		# 空亡，年干不论空亡
		if @bazi.kongwang.indexOf(@bazi[@dizhi[position]].name)>=0 and position!=0
			result=not result
		if result then 1 else -1
	###*
	 * 获取六亲的内环境的用忌
	 * @param  {object} liuqinObject 六亲对象
	 * @return {boolean}              true旺用，false弱忌
	###
	getLiuqinNeiYongji:(liuqinObject)=>
		position=@tiangan.indexOf liuqinObject.zhu
		@tongzhuDizhiToTiangan position
		
	###*
	 * 根据六亲环境论的左右环境判别数组，获取一个需要的六亲环境位置
	 * @param  {number} yinyang             1正，-1偏
	 * @param  {number} positionOfLiuqinWai 六亲的位置
	 * @param  {string} type                social或family
	 * @return {number}                     环境的位置
	###
	getCommonPosition:(yinyang,positionOfLiuqinWai,type)=>
		if not type then type='social'
		zhengpian=if yinyang==1 then 'zheng' else 'pian'
		gender=@bazi.gender.id
		newPosition=@genderMap[gender][zhengpian][type]+positionOfLiuqinWai
		# 六亲在年柱
		if [0,3].indexOf(positionOfLiuqinWai)>=0
			newPosition=@specialMap[positionOfLiuqinWai][gender][zhengpian][type]
		newPosition

	###*
	 * 根据正偏六亲获取一个六亲的外部环境位置
	 * @param  {number} yinyang             1正，-1偏
	 * @param  {number} positionOfLiuqinWai 六亲的位置
	 * @return {number}                     外部环境的位置
	###
	getLiuqinWaiSocial:(yinyang,positionOfLiuqinWai)=>
		@getCommonPosition yinyang,positionOfLiuqinWai,'social'
	
	###*
	 * 根据证偏六亲获取一个六亲的内部环境位置
	 * @param  {number} yinyang             1正，-1偏
	 * @param  {number} positionOfLiuqinWai 六亲的位置
	 * @return {number}                     外部环境的位置
	###
	getLiuqinWaiFamily:(yinyang,positionOfLiuqinWai)=>
		@getCommonPosition yinyang,positionOfLiuqinWai,'family'

	###*
	 * 构建每一个六亲的内外环境
	###
	buildHuanjingForLiuqin:()=>
		_.map @liuqin,(value,key)=>@initEnvForALiuqin key

	###*
	 * 根据当前六亲、环境的位置，以及是内还是外，来判断每一个六亲的环境的用忌
	 * 这里的判断，是内外分开的，是指内环境的左右对内环境的用忌
	 * @param  {object} liuqinObject           六亲对象
	 * @param  {number} huanjingPosition 环境的位置
	 * @param  {string} type             nei或者wai，分别代表内环境（地支）或外环境（天干）
	 * @return {number}                  -1忌，1用
	###
	yongjiOfLiuqinHuanjing:(liuqinObject,huanjingPosition,type)=>
		characterName=if type=='nei' then @dizhi[huanjingPosition] else @tiangan[huanjingPosition]
		huanjing=@bazi[characterName]
		liuqinPosition=@tiangan.indexOf liuqinObject.zhu
		liuqinPositionName=if type=='nei' then @dizhi[@tiangan.indexOf liuqinObject.zhu] else @tiangan[@tiangan.indexOf liuqinObject.zhu]
		liuqin=@bazi[liuqinPositionName]
		#console.log '-----------------------------------'
		#console.log liuqinObject.name,type
		#console.log huanjing.name,liuqin.name
		#console.log huanjingPosition,liuqinPosition
		
		if liuqinPosition-huanjingPosition==1 or liuqinPosition-huanjingPosition==-1
			#console.log "相邻"
			result= if type=='wai' then @XinPaiBasic.tianganWangshuai liuqin,huanjing else @XinPaiBasic.dizhiWangshuai liuqin,huanjing 
			#console.log result
			if result then 1 else -1
		else
			position=0
			if liuqinPosition>huanjingPosition
				position=huanjingPosition+1
			else
				position=huanjingPosition-1
			
			
			
			middleCharacterName=if type=='nei' then @dizhi[position] else @tiangan[position]
			middleCharacter=@bazi[middleCharacterName]

			# 月令空亡的时候，日支可以越过直接和年支作用！
			if @bazi.kongwang.indexOf(middleCharacter=@bazi[middleCharacterName].name)>=0
				result= @XinPaiBasic.dizhiWangshuai liuqin,huanjing 
				#console.log result
				if result then 1 else -1

			# 月令不空亡的时候，需要判断与月令的关系
			else 
				#console.log '开始判断和中间字的关系'
				middleYongjiToNei=@yongjiOfLiuqinHuanjing liuqinObject,position,type
				
				#console.log '隔，中间的字是'+middleCharacter.name+'用忌是'+middleYongjiToNei
				
				if type=='nei'
					relation=@dizhiRelation middleCharacter,huanjing,huanjingPosition==0
				else
					relation=@XinPaiBasic.tianganWangshuai middleCharacter,huanjing
				result=middleYongjiToNei
				#console.log "当前字和中间字的关系是#{relation}"
				if not relation then result=-1*result
				#console.log "#{result}"
			result



	dizhiRelation:(dizhi1Ob,dizhi2Ob,isNianZhi=false)=>
		result=@XinPaiBasic.dizhiWangshuai dizhi1Ob,dizhi2Ob
		if @bazi.kongwang.indexOf(dizhi2Ob.name)>=0 and not isNianZhi then not result else result


exports.HuanJingLun=HuanJingLun

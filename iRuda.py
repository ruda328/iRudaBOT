import asyncio
import discord, os, re, random, sys, time, subprocess, urllib.request
from bs4 import BeautifulSoup

app = discord.Client()

access_token = os.environ["BOT_TOKEN"]
token = access_token

is_server_on = 'true'

@app.event
async def on_ready():
    print("이루다 봇이 다음과 같이 로그인합니다.")
    print(app.user.name)
    print(app.user.id)
    print("=====누출되지 않게 하십시오.=====")
    
# 이루다 봇 게임 하기
    #messages = ['임시서버 가동중', '문의 : 루다#5654']
    #while True:
    #    await app.change_presence(status=discord.Status.online, activity=discord.Game(name=messages[0]))
    #    messages.append(messages.pop(0))
    #    await asyncio.sleep(10)

@app.event
async def on_message(message):
    
    rspd = 0
    id = message.author.id
    channel = message.channel

# 시간모듈
    now = time.localtime()

    now_time = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)
    backup_time = "%04d-%02d-%02d %02d시 %02d분 %02d초" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

    if message.author.bot:
        return None

# 기본명령어
    if is_server_on == 'false':
        if message.content == "이루다 임시서버가동":
            is_server_on = 'true'
            await channel.send("임시서버가동이 시작되었습니다.")
        else:
            return None
    
    if message.content == "이루다 임시서버가동중지":
        is_server_on = 'false'
        await channel.send("임시서버가동이 중지되었습니다.")
    
    if message.content == "이루다":
        rspd = rspd + 1
        await channel.send("네, <@"+str(id)+">님! 저 여기있어요!\n당신이 있는 곳은 `#"+str(channel)+"` 이군요!")

    if message.content == "이루다 도움말":
        await channel.send("현재는 임시서버가 가동중이므로 도움말 기능을 사용할 수 없어요.")
        rspd = rspd + 1

    if message.content == "이루다 호출":
        await channel.send("그럼 호출해볼게요!\n(임시서버 가동중이라서 안 올 확률이 커요.)")
        user = app.get_user(500251192883150859)
        await user.send("주인님! <@"+str(id)+">님이 호출하셨답니다!")
        await channel.send("호출했어요!")
        rspd = rspd + 1

    if message.content.startswith("이루다 따라해"):
        repeat = message.content[8:]
        await channel.send("[이루다 봇] "+str(repeat))
        rspd = rspd + 1

    if message.content == "이루다 내정보":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 어드민리스트":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
    
    if message.content == "이루다 공식사이트":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 공식사이트", description="다음은 이루다 봇의 공식 사이트 주소예요.\n이루다 봇에 대한 자세한 정보를 보실수도 있고, 문제사항에 대해서 문의하실수도 있어요!\n\n공식사이트 [바로가기](https://se701-2201.wixsite.com/irudabot)\n\n새롭게 바뀐 공식사이트 [미리보기](https://www.iruda.kro.kr)")
        await channel.send(embed=embed)

    if message.content.startswith("이루다 DM "):
        rspd = rspd + 1
        if message.content[7:].startswith("<@"):
            target = re.findall(r'\d+', message.content)
            target = target[0]
            target = str(target)

            await channel.send("<@"+target+">님에게 DM을 보냈어요!\n\n수신자 : <@"+str(id)+">님\n\n발신자 : <@"+target+">님\n\n내용 : "+message.content[30:]+"\n\n`위 메시지는 DM명령어 사용건에 대한 개인정보 처리방침을 따라요. 개인정보 처리방침 전문을 조회하려면, '이루다 개인정보처리방침 1'을 입력해주세요.`")
            user = app.get_user(int(target))
            await user.send("<@"+str(id)+">님이 DM을 보냈어요!\n\n수신자 : <@"+str(id)+">님\n\n발신자 : <@"+target+">님\n\n내용 : "+message.content[30:]+"\n\n`위 메시지는 DM명령어 사용건에 대한 개인정보 처리방침을 따라요. 받은 메시지에 부적절한 요소가 포함되어있거나, 개인정보 처리방침 전문을 조회하려면 '이루다 개인정보처리방침 1'을 입력해주세요.`")
        else:
            await channel.send("언급된 대상을 찾지 못했어요ㅜ 메세지를 다시 한번 확인해주세요!")

    if message.content == "이루다 개인정보처리방침 1":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 DM 명령어 개인정보 처리방침", description="다음은 개인정보 처리방침의 전문입니다.\n\n 이루다 봇 DM 명령어(이하 DM 명령어)를 이용할 시, 해당 메시지를 통해 전달된 사항에 대한 책임은 모두 메시지를 전한 본인에게 있으며 이루다 봇 측은 전혀 책임이 없음을 알립니다.\n**DM 명령어로 전송된 모든 메시지는 log파일에 기록되며,** 개인정보 처리방침에 동의하지 않을 시 관리자에게 문의하여 전체 채팅 log를 삭제하실 수 있습니다.\n\n[FAQ]\nQ : DM으로부터 부적절한 메시지, 폭력성, 선정적 음란물 메시지를 받았을 땐 어떻게 해야 하나요?\nA : log 파일을 조회하여 보낸 사용자의 ID를 확보하여 해당 사용자가 더이상 이루다 봇을 이용하지 못하도록 할 수 있습니다. 필요에 따라 증거자료로 남겨둘 수도 있으니, 관리자에게 문의해주시길 바랍니다.")
        await channel.send(embed=embed)

    if message.content == "이루다 초대" or message.content == "이루다 초대코드":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 초대하기", description="이루다 봇을 초대해주셔서 감사합니다 :D\n[여기](https://discord.com/api/oauth2/authorize?client_id=679600384422969367&permissions=8&scope=bot)를 클릭하셔서 봇을 초대하세요!\n\n*초대코드에 문제가 있다고 생각하는 경우 루다#5654님에게 문의해주세요.")
        await channel.send(embed=embed)

    if message.content == "이루다 핑":
        rspd = rspd + 1
        embed = discord.Embed(title=":ping_pong: 퐁!", description=f"이루다 봇의 응답속도는 `{round(app.latency*1000)}ms`입니다.")
        await channel.send(embed=embed)

        return None

    if message.content == "이루다 시계":
        rspd = rspd + 1
        await channel.send("현재 시각을 알려드릴게요. (이루다 봇 서버 시각입니다.)\n```UCT(세계협정시) "+now_time+"```")

    if message.content.startswith("이루다 가르치기 "):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 가르치기삭제 "):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 가르치기목록":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

# 관리자 명령어
    if message.content.startswith("이루다 경고주기"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 어드민추가"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 어드민해제"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 경고해제"):
        rspd = rspd + 1        
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content == "이루다 꺼져":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 서버점검설정"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 백업":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content == "이루다 공지채널등록":
        if auth == 'ad':
           await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content.startswith("이루다 공지쓰기 "):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 공지채널등록해제"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 공지조회":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

# 돈 관련 명령어
    if message.content == "이루다 통장생성":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 사용권계약 1":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 돈 관련 명령어 최종 사용권 계약", description="사용권 계약의 정보는 다음과 같습니다.\n\n 이루다 봇 상에서 존재하는 모든 재화(이하 재화)의 가치는 없습니다. 재화를 이용한 내기, 도박과 같은 실제 화폐를 담보로 한 도박행위로 인해 발생한 피해에 대해서 이루다 봇 측에서는 아무런 책임이 없습니다. 이루다 봇은 자신의 가상계좌에 대한 돈 입금등을 가장한 협박으로부터 해당 사용자가 이루다 봇을 더이상 사용하지 못하게 할 권리가 있으며, 또한 해당 사용자를 서버에서 추방할 권리가 있습니다.\n\n[FAQ]\nQ : 사용자 계약에 동의하지 않으려면 어떻게 하야 하나요?\nA : 이루다봇의 돈 관련 명령어를 사용하지 않으시면 됩니다.\n\nQ : 이미 이루다 돈 명령어를 사용했는데, 나중에 계약을 철회하고 싶다면 어떻게 해야 하나요?\nA : 관리자의 DM으로 계약 철회관련 메시지를 보내시면 됩니다. 단, 이때는 사용자가 계약조건을 단 한번도 위반하지 않았을때 계약철회가 가능합니다.")
        await channel.send(embed=embed)

        f = open("C:/iruda/log/system_log.txt", 'w', encoding="UTF8")
        f.write(log + "\n["+now_time+"] ID "+str(id)+" : 사용권 계약 1 조회")
        f.close()

    if message.content == "이루다 내돈":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content == "이루다 기본배팅":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 돈받기":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 스릴배팅":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 돈선물"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 미친배팅":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content.startswith("이루다 조건배팅"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
# 스톤 관련 명령어
    if message.content == "이루다 스톤":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 모래시계":
        rspd =  rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 스톤구매":
        rspd = rspd + 1
        await channel.send("[스톤 종류별 가격]\nS+ONE `3`개 - `100`원\n S+ONE `18(15+3)`개 - ~~`500`원~~ 할인가: `200`원\n S+ONE `49(45+4)`개 - ~~`1500`원~~ 할인가: `1300`원\n S+ONE `160(150+10)`개 - ~~`5000`원~~ 할인가: `4900`원\n\n구매의향이 있는경우 개발자에게 문의해주세요.\n환불정책에 관해서는 개발자에게 문의해주세요.")
  
    if message.content == "이루다 모래시계구매":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content.startswith("이루다 스톤코드 ") and rspd == 0:
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 스톤충전 "):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
            
    if message.content.startswith("이루다 스톤사용 "):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
#보안
    if message.content == "이루다 본인인증코드발급":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 본인인증코드해제":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")


# 쿠폰코드
    if message.content.startswith("이루다 쿠폰입력"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

#코스피 명령어
    if message.content == "이루다 코스피지수":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content == "이루다 코스피":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content == "이루다 사용권계약 2":
        rspd = rspd + 1
        embed = discord.Embed(title="이루다 봇 코스피 시스템 최종 사용권 계약", description="이루다 봇 내에서 유통 / 판매되는 주식의 가치는 없습니다. 이루다 주식 명령어는 실제 주식을 매수하거나, 매도하는 것이 아니며 이루다 봇 내에서 유통되는 주식은 실제 코스피에 반영되지 않음을 알립니다.\n\n[FAQ]\nQ : 사용자 계약에 동의하지 않으려면 어떻게 하야 하나요?\nA : 이루다 주식 관련 명령어를 사용하지 않으면 됩니다.\n\nQ : 이미 이루다 주식 명령어를 사용했는데, 나중에 계약을 철회하고 싶다면 어떻게 해야 하나요?\nA : 관리자의 DM으로 계약 철회관련 메시지를 보내시면 됩니다. 단, 이때는 사용자가 계약조건을 단 한번도 위반하지 않았을때 계약철회가 가능합니다.")
        await channel.send(embed=embed)
        await channel.send("**사용권 계약에 동의**하고 **주식 명령어를 사용**하고 싶으시다면, '이루다 주식통장생성'명령어를 입력해주세요!")

    if message.content == "이루다 주식통장생성":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content == "이루다 내주식":
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")

    if message.content.startswith("이루다 코스피 매수"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
    if message.content.startswith("이루다 코스피 매도"):
        rspd = rspd + 1
        await channel.send("현재는 임시서버가 가동중이므로 사용할 수 없는 기능이예요.")
        
# 명령어 유효 확인
    if message.content.startswith("이루다 ") and rspd == 0:
        await channel.send("> 제가 대답할 수 있는게 없네요...\n> 혹시 '이루다 도움말'을 사용해서 다시 알아봐주실 수 있나요?")

app.run(token)
